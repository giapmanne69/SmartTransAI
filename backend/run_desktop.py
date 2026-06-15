import sys
import os

# Add the backend directory containing the 'app' package to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import uvicorn
from app.main import app

if __name__ == "__main__":
    # Start the server on localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
