from fastapi import APIRouter, HTTPException

from app.core import logger
from ..core.config import get_settings
from .models import ChatRequest, ChatResponse
from app.agent.agent import Agent, State

# Setup router and logging
router = APIRouter()
settings = get_settings()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest) -> ChatResponse:
    """
    Chat with the Todoist agent
    """
    try:
        logger.info(f"Received {request.type} request with input: {request.input}")
        
        if request.type == "audio":
            logger.warning("Audio input type not implemented")
            raise HTTPException(
                status_code=400,
                detail="Audio input is not implemented yet"
            )
            
        # Process the request through the agent
        logger.info("Starting agent processing")
        result = await Agent.process(request.input)
        
        # if not result["success"]:
        #     logger.error(f"Agent processing failed: {result.get('error', 'Unknown error')}")
        #     raise HTTPException(
        #         status_code=500,
        #         detail=result.get("error", "Unknown error occurred")
        #     )
            
        logger.info("Successfully processed request")
        logger.debug(f"Agent response: {result['response']}")
        
        return ChatResponse(
            success=True,
            details=result["response"]
        )
        
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {e.detail}")
        raise e
    except Exception as e:
        # logger.error(f"Unexpected error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
