import os
import re
import asyncio
from openai import OpenAI

class KimiClient:
    def __init__(self):
        # Configuration OpenRouter
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    
    async def generate_code(self, description: str, stack: str):
        prompt = f"""
        Tu es un architecte logiciel senior. Génère une application complète {stack} pour :
        {description}
        
        **UTILISE POSTGRESQL avec SQLAlchemy (pas MongoDB).**
        - La DATABASE_URL sera fournie via variable d'environnement
        - Utilise `sqlalchemy.create_engine(os.getenv("DATABASE_URL"))`
        - Crée les tables avec `Base.metadata.create_all(bind=engine)`
        
        Retourne UNIQUEMENT des blocs markdown avec `file:chemin/du/fichier`.
        Structure :
        - Frontend complet (React, hooks, routing)
        - Backend complet (FastAPI, SQLAlchemy modèles Pydantic, JWT auth)
        - Schéma PostgreSQL (tables users, items avec migrations)
        - Fichiers config (package.json, requirements.txt, docker-compose.yml, .env.example)
        - README avec instructions
        """
        
        response = self.client.chat.completions.create(
            model="moonshotai/Kimi-K2-Thinking",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=0.2,
            max_tokens=8192,
            top_p=0.95
        )
        
        reasoning_log = []
        final_content = ""
        
        for chunk in response:
            delta = chunk.choices[0].delta
            
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                reasoning_log.append(delta.reasoning_content)
                print(f"💭 {delta.reasoning_content}", end="", flush=True)
            
            if hasattr(delta, 'content') and delta.content:
                final_content += delta.content
        
        return self._parse_code_blocks(final_content)
    
    def _parse_code_blocks(self, content: str):
        regex = r'```file:(.+?)\n(.*?)```'
        return re.findall(regex, content, re.DOTALL)
