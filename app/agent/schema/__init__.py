from typing import Dict, Any

from pydantic import BaseModel

class State(BaseModel):
    input: str
    response: str = ""
    understanding: Dict[str, Any] = {}