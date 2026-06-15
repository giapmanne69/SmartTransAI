import os
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

import sys

if getattr(sys, 'frozen', False):
    # If running in a PyInstaller bundle, use the directory where the executable is located
    base_dir = os.path.dirname(sys.executable)
else:
    # If running in development, use the backend directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SETTINGS_FILE = os.path.join(base_dir, "settings.json")

def get_openrouter_key_from_file() -> str:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                return data.get("OPENROUTER_API_KEY", "")
        except Exception:
            pass
    return os.getenv("OPENROUTER_API_KEY", "")

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smart_trans.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretjwtkeychangeinproduction12345")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # OpenRouter API settings
    OPENROUTER_API_KEY: str = get_openrouter_key_from_file()
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-pro")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

settings = Settings()
