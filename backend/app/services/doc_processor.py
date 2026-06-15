import re
import io
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences using simple regex.
    Cleans up whitespace and returns non-empty sentences.
    """
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Split on terminal punctuation followed by space or end of string
    sentence_end = re.compile(r'(?<=[.!?])\s+')
    raw_sentences = sentence_end.split(text)
    return [s.strip() for s in raw_sentences if s.strip()]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file bytes."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX file bytes."""
    doc = DocxDocument(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs if p.text])

def extract_text_from_txt(file_bytes: bytes) -> str:
    """Extract text from TXT file bytes."""
    return file_bytes.decode("utf-8", errors="ignore")

class DocProcessor:
    @staticmethod
    def process_file(file_name: str, file_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Process a file, extract its text, split into paragraphs,
        sub-split paragraphs into batches of max 10 sentences,
        and construct context windows for each batch.
        """
        ext = file_name.split('.')[-1].lower()
        if ext == 'pdf':
            text = extract_text_from_pdf(file_bytes)
        elif ext in ['docx', 'doc']:
            text = extract_text_from_docx(file_bytes)
        elif ext == 'txt':
            text = extract_text_from_txt(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # 1. Split the text into raw paragraphs
        raw_paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # 2. Extract sentence batches from paragraphs
        batches = []
        for paragraph in raw_paragraphs:
            sentences = split_into_sentences(paragraph)
            if not sentences:
                continue
            
            # Batch sentences (max 10 per batch)
            current_batch = []
            for sentence in sentences:
                current_batch.append(sentence)
                if len(current_batch) == 10:
                    batches.append(" ".join(current_batch))
                    current_batch = []
            if current_batch:
                batches.append(" ".join(current_batch))
                
        # 3. Create chunks with context windows (using prev and next batch as context)
        chunks = []
        num_batches = len(batches)
        
        for i, batch_text in enumerate(batches):
            prev_context = batches[i-1] if i > 0 else ""
            next_context = batches[i+1] if i < num_batches - 1 else ""
            
            context_window = (
                f"[PREVIOUS CONTEXT]\n{prev_context}\n\n"
                f"[CURRENT TEXT]\n{batch_text}\n\n"
                f"[FOLLOWING CONTEXT]\n{next_context}"
            )
            
            chunks.append({
                "original_text": batch_text,
                "context_window": context_window,
                "position_index": i
            })
            
        return chunks
