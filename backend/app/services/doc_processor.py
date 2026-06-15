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
        Process a file, extract its text, split into sentences, 
        and construct context windows for each sentence.
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
        
        sentences = split_into_sentences(text)
        
        chunks = []
        num_sentences = len(sentences)
        
        for i, sentence in enumerate(sentences):
            # Context window: 2 sentences before and 2 sentences after
            start_prev = max(0, i - 2)
            prev_sentences = sentences[start_prev:i]
            
            end_next = min(num_sentences, i + 3)
            next_sentences = sentences[i+1:end_next]
            
            prev_context = " ".join(prev_sentences)
            next_context = " ".join(next_sentences)
            
            context_window = (
                f"[PREVIOUS CONTEXT]\n{prev_context}\n\n"
                f"[CURRENT SENTENCE]\n{sentence}\n\n"
                f"[FOLLOWING CONTEXT]\n{next_context}"
            )
            
            chunks.append({
                "original_text": sentence,
                "context_window": context_window,
                "position_index": i
            })
            
        return chunks
