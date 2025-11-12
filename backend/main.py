from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from contextlib import contextmanager
from orchestrator.generator import AppGenerator
from orchestrator.models import ProjectRequest

app = FastAPI(title="OK Computer Clone", version="1.0.0")

# CONFIG CORS POUR VERCEL ET LOCAL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app-generator-sigma.vercel.app",  # Remplace * par ton ID Vercel
        "http://localhost:3000"
    ],
    allow_credentials=True,
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
        if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
