from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import urllib.request
import json
import os
import threading

router = APIRouter(prefix="/settings", tags=["settings"])

from ..core.config import SETTINGS_FILE

# Global dictionary to keep track of model pulling progress
pull_status = {
    "status": "idle", # "idle", "downloading", "success", "error"
    "progress": 0,
    "message": ""
}

class SaveSettingsRequest(BaseModel):
    openrouter_api_key: str

def check_ollama_running() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/", timeout=2) as response:
            return response.status == 200
    except Exception:
        return False

def check_model_downloaded() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                models = data.get("models", [])
                for model in models:
                    name = model.get("name", "")
                    if name.startswith("llama3") or "llama3" in name:
                        return True
    except Exception:
        pass
    return False

def pull_model_task():
    global pull_status
    pull_status["status"] = "downloading"
    pull_status["progress"] = 0
    pull_status["message"] = "Bắt đầu tải mô hình..."
    
    url = "http://127.0.0.1:11434/api/pull"
    payload = json.dumps({"name": "llama3"}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        # Note: Ollama pull endpoint streams the progress line-by-line
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    data = json.loads(line.decode('utf-8'))
                    status_text = data.get("status", "")
                    completed = data.get("completed", 0)
                    total = data.get("total", 0)
                    
                    pull_status["message"] = status_text
                    if total > 0:
                        pull_status["progress"] = int((completed / total) * 100)
                    else:
                        pull_status["progress"] = 0
            
            pull_status["status"] = "success"
            pull_status["progress"] = 100
            pull_status["message"] = "Đã tải xong mô hình Llama-3!"
    except Exception as e:
        pull_status["status"] = "error"
        pull_status["message"] = f"Lỗi khi tải mô hình: {str(e)}"

@router.get("/status")
def get_settings_status():
    ollama_running = check_ollama_running()
    model_downloaded = check_model_downloaded() if ollama_running else False
    
    # Check if OpenRouter key is set
    openrouter_key = ""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                openrouter_key = data.get("OPENROUTER_API_KEY", "")
        except Exception:
            pass
    if not openrouter_key:
        openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        
    return {
        "ollama_running": ollama_running,
        "model_downloaded": model_downloaded,
        "openrouter_key_set": len(openrouter_key) > 0,
        "pull_status": pull_status
    }

@router.post("/save")
def save_settings(req_data: SaveSettingsRequest):
    data = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            pass
            
    data["OPENROUTER_API_KEY"] = req_data.openrouter_api_key
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể lưu file cấu hình: {str(e)}"
        )
        
    # Update in-memory configuration settings
    from ..core.config import settings
    settings.OPENROUTER_API_KEY = req_data.openrouter_api_key
    
    return {"status": "success", "message": "Đã lưu cấu hình API Key thành công."}

@router.post("/pull-model")
def trigger_pull_model():
    if not check_ollama_running():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ollama chưa chạy. Vui lòng bật Ollama trước."
        )
        
    global pull_status
    if pull_status["status"] == "downloading":
        return {"status": "already_running", "message": "Tiến trình tải mô hình đang diễn ra."}
        
    thread = threading.Thread(target=pull_model_task)
    thread.daemon = True
    thread.start()
    return {"status": "started", "message": "Bắt đầu tải mô hình Llama-3 trong nền."}
