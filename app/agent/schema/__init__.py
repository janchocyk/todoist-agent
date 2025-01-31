from typing import Dict, Any, List

from pydantic import BaseModel

class State(BaseModel):
    input: str
    response: str = ""
    understanding: Dict[str, Any] = {}
    steps: List[str] = []
    go_tool: bool = False
    tool_calls: List = []
    final_response: str = ""