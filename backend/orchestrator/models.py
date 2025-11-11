from pydantic import BaseModel

class ProjectRequest(BaseModel):
    description: str
    stack: str
    name: str

class ProjectStatus(BaseModel):
    project_id: str
    status: str
    logs: list[str] = []
