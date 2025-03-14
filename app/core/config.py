from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import Field
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv(), override=True)

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    LANGFUSE_SECRET_KEY: str = Field(..., env="LANGFUSE_SECRET_KEY")
    LANGFUSE_PUBLIC_KEY: str = Field(..., env="LANGFUSE_PUBLIC_KEY")
    LANGFUSE_HOST: str = Field(..., env="LANGFUSE_HOST")
    TODOIST_API_KEY: str = Field(..., env="TODOIST_API_KEY")
    
    # App settings
    APP_NAME: str = "Todoist Agent"
    API_V1_STR: str = "/api/v1"
    
    # Agent Settings
    MODEL_NAME: str = "claude-3-5-sonnet-20241022"
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 4096
    
    class Config:
        # env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings
