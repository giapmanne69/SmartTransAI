import re
import math
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import Glossary, DocumentChunk, Document

class VectorService:
    @staticmethod
    def get_character_ngram_vector(text: str, all_ngrams: List[str]) -> List[int]:
        """
        Creates a simple character n-gram bag-of-words vector as a Python list.
        """
        text = text.lower()
        vector = [0] * len(all_ngrams)
        for i, ngram in enumerate(all_ngrams):
            vector[i] = text.count(ngram)
        return vector

    @staticmethod
    def calculate_cosine_similarity(v1: List[int], v2: List[int]) -> float:
        """Calculate cosine similarity between two numeric lists."""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(a * a for a in v1))
        norm_v2 = math.sqrt(sum(b * b for b in v2))
        
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return dot_product / (norm_v1 * norm_v2)

    @classmethod
    def retrieve_glossary_for_text(cls, db: Session, user_id: int, text: str, threshold: float = 0.2) -> List[Dict[str, Any]]:
        """
        Retrieve glossary terms matching the text.
        Combines strict keyword matching (exact match) and character n-gram cosine similarity (RAG).
        """
        # Fetch glossary items from database
        items = db.query(Glossary).filter(Glossary.user_id == user_id).all()
        if not items:
            return []

        matched_items = []
        text_lower = text.lower()

        # 1. Exact Substring Matching (Crucial for glossary lookup)
        for item in items:
            term = item.source_term.lower()
            # Simple word-boundary check to avoid matching parts of other words (e.g. 'cat' in 'category')
            pattern = rf"\b{re.escape(term)}\b"
            if re.search(pattern, text_lower) or term in text_lower:
                matched_items.append({
                    "id": item.id,
                    "source_term": item.source_term,
                    "target_term": item.target_term,
                    "notes": item.notes,
                    "match_type": "exact"
                })

        # 2. Vector Cosine Similarity Fallback (if no exact matches, or for fuzzy finding)
        if not matched_items and len(items) > 0:
            # Create a dynamic vocabulary of 3-grams from all glossary terms
            all_ngrams = set()
            for item in items:
                term = item.source_term.lower()
                for j in range(len(term) - 2):
                    all_ngrams.add(term[j:j+3])
            
            all_ngrams = list(all_ngrams)
            if all_ngrams:
                text_vector = cls.get_character_ngram_vector(text, all_ngrams)
                
                for item in items:
                    item_vector = cls.get_character_ngram_vector(item.source_term, all_ngrams)
                    similarity = cls.calculate_cosine_similarity(text_vector, item_vector)
                    
                    if similarity >= threshold:
                        matched_items.append({
                            "id": item.id,
                            "source_term": item.source_term,
                            "target_term": item.target_term,
                            "notes": item.notes,
                            "match_type": f"fuzzy (sim: {similarity:.2f})"
                        })

        # Remove duplicates
        seen_ids = set()
        unique_matches = []
        for match in matched_items:
            if match["id"] not in seen_ids:
                seen_ids.add(match["id"])
                unique_matches.append(match)

        return unique_matches

    @classmethod
    def retrieve_past_corrections(cls, db: Session, user_id: int, text: str, limit: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves past translation corrections edited by the human reviewer.
        Serves as a dynamic dynamic-few-shot training/fine-tuning loop for LLM context.
        """
        # Fetch chunks that were manually edited by this user
        corrected_chunks = db.query(DocumentChunk).join(Document).filter(
            Document.user_id == user_id,
            DocumentChunk.corrected_by_user == True,
            DocumentChunk.translated_text != None
        ).all()
        
        if not corrected_chunks:
            return []
            
        matches = []
        text_lower = text.lower()
        
        # Build n-grams of all target terms to compute similarity
        all_ngrams = set()
        for j in range(len(text_lower) - 2):
            all_ngrams.add(text_lower[j:j+3])
            
        for cc in corrected_chunks:
            cc_lower = cc.original_text.lower()
            for j in range(len(cc_lower) - 2):
                all_ngrams.add(cc_lower[j:j+3])
                
        all_ngrams_list = list(all_ngrams)
        if not all_ngrams_list:
            return []
            
        text_vector = cls.get_character_ngram_vector(text, all_ngrams_list)
        
        for cc in corrected_chunks:
            # Skip exact sentence match to avoid self-referencing if translating same document chunk
            if cc.original_text == text:
                continue
                
            cc_vector = cls.get_character_ngram_vector(cc.original_text, all_ngrams_list)
            sim = cls.calculate_cosine_similarity(text_vector, cc_vector)
            
            if sim >= 0.15: # threshold to consider relevant examples
                matches.append((sim, cc))
                
        # Sort by similarity descending
        matches.sort(key=lambda x: x[0], reverse=True)
        
        return [
            {
                "original_text": cc.original_text,
                "translated_text": cc.translated_text
            }
            for sim, cc in matches[:limit]
        ]

