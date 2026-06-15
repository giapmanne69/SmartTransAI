from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth, glossary, document, settings as settings_api

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Trans AI API",
    description="Backend API for Smart Trans AI - AI Agentic Computer-Assisted Translation Tool",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(glossary.router, prefix="/api")
app.include_router(document.router, prefix="/api")
app.include_router(settings_api.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": "Smart Trans AI",
        "description": "Agentic translation CAT Tool system is running."
    }

# Serve React frontend static files if built
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # In PyInstaller bundle, static files are extracted to sys._MEIPASS
    frontend_dist = os.path.join(sys._MEIPASS, "frontend", "dist")
else:
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    frontend_dist = os.path.join(project_root, "frontend", "dist")

if os.path.exists(frontend_dist):
    # Mount assets folder
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    # Catch-all to support SPA routing
    @app.get("/{catchall:path}")
    def serve_frontend(catchall: str):
        # Prevent catching API routes
        if catchall.startswith("api") or catchall.startswith("docs") or catchall.startswith("redoc") or catchall.startswith("openapi.json"):
            return None
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend build files not found."}
