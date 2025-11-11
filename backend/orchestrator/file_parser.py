import aiofiles
from pathlib import Path

class FileParser:
    def __init__(self, project_path: Path):
        self.project_path = project_path
    
    async def write_files(self, code_blocks):
        """Écrit chaque fichier sur le disque"""
        for file_path, content in code_blocks:
            full_path = self.project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
                await f.write(content)
