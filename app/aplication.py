from fastapi import FastAPI
from app.api.endpoints import router
from app.core.config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Todoist Task Management Agent",
    version="0.1.0",
    description="Todoist Task Management Agent API"
)

# Add routes
app.include_router(router, prefix=settings.API_V1_STR)