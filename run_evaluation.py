import os
import sys
import json
import re
import math
import subprocess

# Ensure we configure the Python path to load backend app correctly
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Check and install required libraries from backend/requirements.txt + nltk automatically
required_libs = [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("sqlalchemy", "sqlalchemy"),
    ("pydantic", "pydantic"),
    ("langchain_core", "langchain-core"),
    ("langchain_openai", "langchain-openai"),
    ("langgraph", "langgraph"),
    ("PyPDF2", "PyPDF2"),
    ("docx", "python-docx"),
    ("passlib", "passlib[bcrypt]"),
    ("jwt", "pyjwt"),
    ("multipart", "python-multipart"),
    ("dotenv", "python-dotenv"),
    ("nltk", "nltk")
]

missing_packages = []
for module_name, package_name in required_libs:
    try:
        __import__(module_name)
    except ImportError:
        missing_packages.append(package_name)

if missing_packages:
    print(f"Missing required packages for evaluation: {missing_packages}")
    print("Installing missing dependencies automatically via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("All dependencies installed successfully!")
    except Exception as e:
        print(f"Failed to install dependencies automatically: {str(e)}")
        print("Please run manually: pip install -r backend/requirements.txt nltk")
        sys.exit(1)

import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Download necessary NLTK packages
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

# Override environment variables for database to keep it clean and isolated
os.environ["DATABASE_URL"] = "sqlite:///./evaluation_test.db"

# Explicitly load .env from backend/ directory to ensure settings are loaded correctly from project root
import dotenv
dotenv_path = os.path.join(project_root, "backend", ".env")
if os.path.exists(dotenv_path):
    dotenv.load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

# Check OpenRouter API key quota connectivity before running to avoid DNS hangs and 402 timeouts
print("Checking OpenRouter API connectivity and quota...")
api_working = False
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key:
    import urllib.request
    import json
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/auth/key",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
        # 3 second timeout for quick check
        with urllib.request.urlopen(req, timeout=3.0) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            limit = res_data.get("data", {}).get("limit", 0)
            usage = res_data.get("data", {}).get("usage", 0)
            if limit > usage or (limit == 0 and res_data.get("data", {}).get("is_free", False)) or res_data.get("data", {}).get("total_credits", 0) > 0:
                api_working = True
                print("-> OpenRouter API key is valid and has remaining quota.")
            else:
                print("-> OpenRouter API key has insufficient credits/quota.")
    except Exception as e:
        print(f"-> OpenRouter API connectivity/auth check failed: {str(e)}")
else:
    print("-> No OpenRouter API key configured.")

if not api_working:
    print("-> Activating Fast Offline Fallback Mode: OpenRouter LLM calls will fail fast without network delays.")
    import app.llm_provider
    def patched_get_llm(*args, **kwargs):
        raise ValueError("OpenRouter offline fallback mode active (insufficient credits or no connection).")
    app.llm_provider.get_llm = patched_get_llm
    app.llm_provider.get_local_llm = patched_get_llm

from app.database import SessionLocal, engine, Base
from app.models import User, Document, DocumentChunk, Glossary
from app.api.document import translate_single_chunk
from app.services.vector_service import VectorService

# Define custom fallback metrics if NLTK fails
def tokenize_vietnamese(text):
    # Basic word tokenization for evaluation
    text = text.lower()
    return re.findall(r'\b\w+\b', text)

def calculate_ter(candidate: str, reference: str) -> float:
    """
    Calculates Word Error Rate / Translation Edit Rate (without shift operations)
    using Levenshtein distance on tokenized strings.
    """
    cand_tokens = tokenize_vietnamese(candidate)
    ref_tokens = tokenize_vietnamese(reference)
    
    if not ref_tokens:
        return 1.0 if cand_tokens else 0.0
        
    n = len(cand_tokens)
    m = len(ref_tokens)
    
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if cand_tokens[i-1] == ref_tokens[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,    # Deletion
                    dp[i][j-1] + 1,    # Insertion
                    dp[i-1][j-1] + 1   # Substitution
                )
                
    edit_dist = dp[n][m]
    return min(1.0, edit_dist / m)

def calculate_gcr(original: str, candidate: str, glossary_items: list) -> tuple:
    """
    Computes matches and opportunities for Glossary Compliance Rate (GCR).
    """
    orig_lower = original.lower()
    cand_lower = candidate.lower()
    
    opportunities = 0
    matches = 0
    
    for item in glossary_items:
        src = item.source_term.lower()
        tgt = item.target_term.lower()
        
        # Word boundary search to prevent matching parts of words
        pattern = rf"\b{re.escape(src)}\b"
        if re.search(pattern, orig_lower) or src in orig_lower:
            opportunities += 1
            if tgt in cand_lower:
                matches += 1
                
    return matches, opportunities

def calculate_bleu(candidate: str, reference: str) -> float:
    """
    Computes BLEU score using NLTK sentence_bleu with smoothing.
    """
    cand_tokens = tokenize_vietnamese(candidate)
    ref_tokens = [tokenize_vietnamese(reference)]
    
    chencherry = SmoothingFunction()
    # If candidate is too short, fall back to low weights or simple precision
    if len(cand_tokens) < 4:
        weights = (0.5, 0.5, 0.0, 0.0)
    else:
        weights = (0.25, 0.25, 0.25, 0.25)
        
    try:
        return sentence_bleu(ref_tokens, cand_tokens, weights=weights, smoothing_function=chencherry.method1)
    except Exception:
        # Fallback to simple 1-gram precision if nltk fails
        cand_counts = {}
        for t in cand_tokens:
            cand_counts[t] = cand_counts.get(t, 0) + 1
        ref_counts = {}
        for t in ref_tokens[0]:
            ref_counts[t] = ref_counts.get(t, 0) + 1
            
        matched = 0
        for t, count in cand_counts.items():
            if t in ref_counts:
                matched += min(count, ref_counts[t])
        
        return matched / len(cand_tokens) if cand_tokens else 0.0

def main():
    print("======================================================================")
    print("        STARTING ACADEMIC TRANSLATION EVALUATION PIPELINE             ")
    print("======================================================================")

    # 1. Initialize DB tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Clear previous records to ensure clean slate
        db.query(DocumentChunk).delete()
        db.query(Document).delete()
        db.query(Glossary).delete()
        db.query(User).delete()
        db.commit()
        
        # 2. Setup mock evaluator user
        evaluator = User(username="evaluator", hashed_password="mock_password_hash")
        db.add(evaluator)
        db.commit()
        db.refresh(evaluator)
        
        # 3. Load Glossary database
        glossary_path = os.path.join(project_root, "data", "glossary.json")
        if not os.path.exists(glossary_path):
            print(f"Error: glossary file not found at {glossary_path}")
            return
            
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary_data = json.load(f)
            
        glossary_items = []
        for item in glossary_data:
            g = Glossary(
                user_id=evaluator.id,
                source_term=item["source_term"],
                target_term=item["target_term"],
                notes=item.get("notes", "")
            )
            db.add(g)
            glossary_items.append(g)
        db.commit()
        print(f"-> Successfully loaded {len(glossary_data)} glossary terms into database.")
        
        # 4. Load Academic Input Sentences and Ground Truths
        input_path = os.path.join(project_root, "data", "input_academic.txt")
        gt_path = os.path.join(project_root, "data", "ground_truth.json")
        
        if not os.path.exists(input_path) or not os.path.exists(gt_path):
            print("Error: Input sentences or Ground Truth translations missing.")
            return
            
        with open(input_path, "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f if line.strip()]
            
        with open(gt_path, "r", encoding="utf-8") as f:
            ground_truths = json.load(f)
            
        if len(sentences) != len(ground_truths):
            print("Warning: Count mismatch between input sentences and ground truths.")
            
        # 5. Define documents for each translation mode
        modes = ["proposed", "baseline_a", "baseline_b"]
        mode_names = {
            "proposed": "Smart Trans AI (Proposed Agentic + RAG)",
            "baseline_a": "Baseline A (Gemini 1.5 Pro Zero-Shot)",
            "baseline_b": "Baseline B (GPT-4o Mini Zero-Shot)"
        }
        
        documents = {}
        for m in modes:
            doc = Document(
                name=f"Evaluation Doc - {m.upper()}",
                file_path="mock_path",
                file_type="txt",
                status="processing",
                user_id=evaluator.id
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)
            documents[m] = doc
            
            # Create chunks with simple surrounding contexts
            for idx, text in enumerate(sentences):
                # Simple context window: 1 sentence before and after
                prev_sent = sentences[idx-1] if idx > 0 else ""
                next_sent = sentences[idx+1] if idx < len(sentences)-1 else ""
                context_win = f"{prev_sent} {text} {next_sent}".strip()
                
                chunk = DocumentChunk(
                    document_id=doc.id,
                    original_text=text,
                    context_window=context_win,
                    position_index=idx,
                    status="pending"
                )
                db.add(chunk)
            db.commit()

        # 6. Execute Translations
        results_data = {m: [] for m in modes}
        
        print("\nStarting LLM calls. This may take some time depending on API keys and rates...")
        for m in modes:
            print(f"\n>> RUNNING TRANSLATION MODE: {mode_names[m]}")
            doc = documents[m]
            
            # Fetch chunks
            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).order_by(DocumentChunk.position_index).all()
            for chunk in chunks:
                print(f"   Translating sentence {chunk.position_index + 1}/{len(chunks)}...")
                # We call the translate_single_chunk helper directly using a DB session factory
                translate_single_chunk(
                    chunk_id=chunk.id,
                    user_id=evaluator.id,
                    db_session_factory=SessionLocal,
                    mode=m
                )
                
                # Fetch translated chunk
                db.refresh(chunk)
                results_data[m].append({
                    "original": chunk.original_text,
                    "translation": chunk.translated_text or "[Translation Failed]",
                    "reviewer_feedback": chunk.reviewer_feedback
                })
                
        # 7. Metrics calculation
        eval_metrics = {m: {"bleu": [], "ter": [], "gcr_matches": 0, "gcr_opps": 0} for m in modes}
        
        for m in modes:
            for idx, res in enumerate(results_data[m]):
                if idx >= len(ground_truths):
                    break
                ref = ground_truths[idx]
                cand = res["translation"]
                orig = res["original"]
                
                bleu = calculate_bleu(cand, ref)
                ter = calculate_ter(cand, ref)
                gcr_m, gcr_o = calculate_gcr(orig, cand, glossary_items)
                
                eval_metrics[m]["bleu"].append(bleu)
                eval_metrics[m]["ter"].append(ter)
                eval_metrics[m]["gcr_matches"] += gcr_m
                eval_metrics[m]["gcr_opps"] += gcr_o

        # Calculate averages
        report_lines = []
        report_lines.append("# BÁO CÁO KẾT QUẢ THỰC NGHIỆM ĐỐI SÁNH DỊCH THUẬT\n")
        report_lines.append(f"Hệ thống đã chạy thử nghiệm dịch thuật tự động trên {len(sentences)} phân đoạn câu học thuật chuyên ngành CNTT.\n")
        report_lines.append("| Phương pháp đánh giá | BLEU Score ↑ | TER Rate ↓ | Glossary Compliance (GCR) ↑ |")
        report_lines.append("| :--- | :---: | :---: | :---: |")
        
        print("\n" + "="*70)
        print("                        EVALUATION SUMMARY                        ")
        print("="*70)
        print(f"{'Method':<45} | {'BLEU':<8} | {'TER':<8} | {'GCR':<8}")
        print("-"*70)
        
        final_summary_data = {}
        for m in modes:
            avg_bleu = sum(eval_metrics[m]["bleu"]) / len(eval_metrics[m]["bleu"]) if eval_metrics[m]["bleu"] else 0.0
            avg_ter = sum(eval_metrics[m]["ter"]) / len(eval_metrics[m]["ter"]) if eval_metrics[m]["ter"] else 0.0
            
            gcr_opps = eval_metrics[m]["gcr_opps"]
            gcr_rate = (eval_metrics[m]["gcr_matches"] / gcr_opps * 100.0) if gcr_opps > 0 else 100.0
            
            final_summary_data[m] = {
                "bleu": avg_bleu,
                "ter": avg_ter,
                "gcr": gcr_rate
            }
            
            print(f"{mode_names[m]:<45} | {avg_bleu:.4f}   | {avg_ter:.4f}   | {gcr_rate:.2f}%")
            report_lines.append(f"| {mode_names[m]} | {avg_bleu*100:.2f}% | {avg_ter:.2f} | {gcr_rate:.2f}% ({eval_metrics[m]['gcr_matches']}/{gcr_opps}) |")
            
        print("="*70)
        
        # Detail outputs by sentence
        report_lines.append("\n## CHI TIẾT BẢN DỊCH TỪNG PHÂN ĐOẠN CÂU\n")
        for idx, text in enumerate(sentences):
            ref = ground_truths[idx] if idx < len(ground_truths) else ""
            report_lines.append(f"### Câu {idx + 1}:")
            report_lines.append(f"- **Original (English):** *\"{text}\"*")
            report_lines.append(f"- **Ground Truth (Human):** *\"{ref}\"*")
            for m in modes:
                cand = results_data[m][idx]["translation"]
                feedback = results_data[m][idx]["reviewer_feedback"]
                report_lines.append(f"- **{mode_names[m]}:** \"{cand}\"")
                if m == "proposed":
                    report_lines.append(f"  *Phản hồi Reviewer:* {feedback}")
            report_lines.append("")

        # Save Report file
        report_path = os.path.join(project_root, "data", "evaluation_results.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        
        print(f"\n-> Evaluation completed successfully. Full markdown report saved to: {report_path}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
