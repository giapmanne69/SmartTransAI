import multiprocessing
import sys
import os

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Prevent infinite loop spawn of child processes by multiprocessing/loky/torch.
    # Tauri sidecar is always executed with exactly 1 port argument (e.g. "8000").
    is_main = False
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
            if 1024 <= port <= 65535:
                is_main = True
        except ValueError:
            pass
            
    if not is_main:
        sys.exit(0)

# Disable tokenizer and joblib parallelisms to prevent subprocess spawns on Windows
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
os.environ["LOKY_MAX_CPU_COUNT"] = "1"

# Add the backend directory containing the 'app' package to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(sys.argv[1])
    # Start the server on localhost
    uvicorn.run(app, host="127.0.0.1", port=port)


