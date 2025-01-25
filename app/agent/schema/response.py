from pydantic import BaseModel
from typing import Optional

class AgentResponse(BaseModel):
    _thinking: str
    add: Optional[str] = None
    update: Optional[str] = None
    complete: Optional[str] = None
    delete: Optional[str] = None
    list: Optional[str] = None
    get: Optional[str] = None

class ExecuteResponse(BaseModel):
    tool_name: str
    arguments: dict

