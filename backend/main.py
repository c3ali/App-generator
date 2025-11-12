from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from contextlib import contextmanager
from orchestrator.generator import AppGenerator
from orchestrator.models import ProjectRequest

app = FastAPI(title="OK Computer Clone", version="1.0.0")

# CONFIG CORS POUR RAILWAY ET LOCAL
# TEMPORAIRE : Autoriser toutes les origines pour debugger
allowed_origins = ["*"]

# Log pour debug
print(f"🔍 CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # IMPORTANT : doit être False avec allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = AppGenerator()

@app.post("/api/generate")
async def generate_app(request: ProjectRequest):
    """Génère une application complète"""
    try:
        project_id = await generator.create_project(
            description=request.description,
            stack=request.stack,
            name=request.name
        )
        return {"project_id": project_id, "status": "generating"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@contextmanager
def get_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

@app.get("/health")
async def health_check():
    """Vérifie la connexion DB"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            return {"status": "healthy", "db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB error: {str(e)}")
