import os
import sys

class NMTService:
    _tokenizer = None
    _model = None

    @classmethod
    def get_model_and_tokenizer(cls):
        """
        Lazily initializes the translation model and tokenizer directly
        without relying on HF pipeline tasks.
        """
        if cls._model is None or cls._tokenizer is None:
            required = ["transformers", "sentencepiece", "sacremoses", "torch"]
            missing = []
            for lib in required:
                try:
                    if lib == "torch":
                        import torch
                    else:
                        __import__(module_name_map.get(lib, lib))
                except ImportError:
                    missing.append(lib)
            
            if missing:
                print(f"Installing missing offline NMT libraries: {missing}")
                import subprocess
                cmd = [sys.executable, "-m", "pip", "install"]
                if "torch" in missing:
                    cmd += ["torch", "--extra-index-url", "https://download.pytorch.org/whl/cpu"]
                    missing.remove("torch")
                if missing:
                    cmd += missing
                subprocess.check_call(cmd)
            
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            model_name = "Helsinki-NLP/opus-mt-en-vi"
            print(f"Loading {model_name} tokenizer and model offline...")
            cls._tokenizer = AutoTokenizer.from_pretrained(model_name)
            cls._model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
        return cls._model, cls._tokenizer

    @classmethod
    def translate(cls, text: str) -> str:
        if not text.strip():
            return text
        try:
            model, tokenizer = cls.get_model_and_tokenizer()
            # Tokenize input text
            inputs = tokenizer(text, return_tensors="pt", padding=True)
            # Generate translation ids
            translated_ids = model.generate(**inputs)
            # Decode to text
            translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
            return translated_text.strip()
        except Exception as e:
            print(f"NMT offline translation failed: {str(e)}")
            return text

# Mapping of package names to import names if they differ
module_name_map = {
    "python-docx": "docx",
}
