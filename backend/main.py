from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from orchestrator.generator import AppGenerator
from orchestrator.models import ProjectRequest, ProjectStatus

app = FastAPI(title="OK Computer Clone", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """Stream les logs en temps réel"""
    await websocket.accept()
    await generator.stream_logs(project_id, websocket)
