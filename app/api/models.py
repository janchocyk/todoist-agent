from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal

class ChatRequest(BaseModel):
    input: str
    type: Literal["text", "audio"] = "text"

class ChatResponse(BaseModel):
    success: bool
    details: str = Field(description="The response message from the agent")
    error: Optional[str] = None

class AgentRequest(BaseModel):
    input: str
    type: Literal["text", "audio"] = "text"
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    success: bool
    action_taken: str
    details: Dict[str, Any]
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None
