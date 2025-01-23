import pytest
import pytest_asyncio
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os
import asyncio
from httpx import AsyncClient
from fastapi import FastAPI

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from main import app
from app.tools.todoist.tasks import TodoistTools

# Load test environment variables
load_dotenv(".env.test")

@pytest_asyncio.fixture
async def client():
    """Async client fixture"""
    async with AsyncClient(transport=TestClient(app).transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def test_project_id():
    """Test project ID fixture"""
    return os.getenv("TEST_PROJECT_ID")

@pytest.fixture
def test_task_data():
    """Test task data fixture"""
    return {
        "title": "Test Task",
        "due_date": "today",
        "priority": 1
    }

@pytest_asyncio.fixture
async def todoist_tools():
    """Todoist tools fixture"""
    tools = TodoistTools()
    yield tools 