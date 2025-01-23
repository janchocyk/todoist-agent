import asyncio
import sys
from pathlib import Path
from loguru import logger

# Add app directory to Python path
app_dir = str(Path(__file__).resolve().parents[1])
if app_dir not in sys.path:
    sys.path.append(app_dir)

print(sys.path)

from app.agent.prompts import prompt

async def main():
    """Main async function"""
    prompt_result = await prompt()
    logger.info(prompt_result)
    pass

if __name__ == "__main__":
    asyncio.run(main())
