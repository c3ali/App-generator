import os
import re
import asyncio
import subprocess
from pathlib import Path
from orchestrator.llm_client import KimiClient
from orchestrator.file_parser import FileParser

class AppGenerator:
    def __init__(self):
        self.projects_dir = Path("generated_projects")
        self.projects_dir.mkdir(exist_ok=True)
        self.kimi = KimiClient()
        
    async def create_project(self, description: str, stack: str, name: str):
        project_id = f"{name}_{int(asyncio.get_event_loop().time())}"
        project_path = self.projects_dir / project_id
        project_path.mkdir()
        
        code_blocks = await self.kimi.generate_code(description, stack)
        
        parser = FileParser(project_path)
        await parser.write_files(code_blocks)
        
        asyncio.create_task(self._bootstrap_project(project_path, stack))
        
        return project_id
    
    async def _bootstrap_project(self, path: Path, stack: str):
        logs_file = path / "deployment.log"
        
        cmds = [
            ("Installing frontend...", "cd frontend && npm install"),
            ("Installing backend...", "cd backend && npm install"),
            ("Starting database...", "docker-compose up -d mongodb"),
            ("Starting dev servers...", "cd .. && npm run dev:all")
        ]
        
        for step, cmd in cmds:
            await self._run_command(cmd, path, logs_file, step)
    
    async def _run_command(self, cmd: str, cwd: Path, log_file: Path, step: str):
        process = await asyncio.create_subprocess_shell(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        async for line in process.stdout:
            with open(log_file, "a") as f:
                f.write(f"{step}: {line.decode()}\n")
    
    async def stream_logs(self, project_id: str, websocket):
        # Logique de streaming WebSocket (simplifiée)
        await websocket.send_text("Logs en temps réel...")
