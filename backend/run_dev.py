import os
import sys
import uvicorn

# Add the backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    # Disable tokenizers/joblib parallelisms to prevent subprocess loops on Windows
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["JOBLIB_MULTIPROCESSING"] = "0"
    os.environ["LOKY_MAX_CPU_COUNT"] = "1"
    
    print("\n--- Starting FastAPI Backend Server in Development Mode ---")
    print("Address: http://127.0.0.1:8000")
    
    # Run uvicorn via python script to properly manage KeyboardInterrupt signals on Windows
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
