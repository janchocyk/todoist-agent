import sys
from loguru import logger
from pathlib import Path

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure default logger format
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "colorize": True,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": "INFO"
            },
            {
                "sink": "logs/app.log",
                "rotation": "500 MB",
                "retention": "10 days",
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                "level": "DEBUG"
            },
            {
                "sink": "logs/error.log",
                "rotation": "100 MB",
                "retention": "10 days",
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                "level": "ERROR"
            }
        ]
    )
    
    return logger
