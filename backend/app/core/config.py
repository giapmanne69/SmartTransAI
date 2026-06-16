import os
import json
from dotenv import load_dotenv

# Tắt đa luồng của HuggingFace tokenizers và các thư viện khác để tránh lỗi spawn multiprocessing trên Windows
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
os.environ["LOKY_MAX_CPU_COUNT"] = "1"

# Load .env file
load_dotenv()

import sys


if getattr(sys, 'frozen', False):
    # For packaged desktop applications, use the user's AppData directory (Windows) or Home directory (Linux/macOS)
    if sys.platform == "win32":
        base_dir = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "SmartTransAI")
    else:
        base_dir = os.path.join(os.path.expanduser("~"), ".smarttransai")
else:
    # Đi ngược lên 4 cấp để ra Project Root (E:\Project\SmartTransAI) tránh việc watchfiles của uvicorn reload liên tục khi ghi log/db
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Ensure the data directory exists
os.makedirs(base_dir, exist_ok=True)

SETTINGS_FILE = os.path.join(base_dir, "settings.json")
LOG_FILE = os.path.join(base_dir, "smart_trans.log")


def get_openrouter_key_from_file() -> str:
    key = ""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                key = data.get("OPENROUTER_API_KEY", "")
        except Exception:
            pass
    return key if key else os.getenv("OPENROUTER_API_KEY", "")

class Settings:
    @property
    def DATABASE_URL(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
        db_path = os.path.join(base_dir, "smart_trans.db")
        db_path_abs = os.path.abspath(db_path).replace("\\", "/")
        return f"sqlite:///{db_path_abs}"

    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretjwtkeychangeinproduction12345")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # OpenRouter API settings
    OPENROUTER_API_KEY: str = get_openrouter_key_from_file()
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-pro")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

settings = Settings()
