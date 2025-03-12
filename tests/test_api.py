import pytest
from httpx import AsyncClient
from app.__main__ import app

@pytest.mark.asyncio
async def test_chat_endpoint_text(client):
    """Test chat endpoint with text input"""
    response = await client.post(
        "/api/v1/chat",
        json={
            "input": "Create a task called 'Test API' due tomorrow",
            "type": "text"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "details" in data

@pytest.mark.asyncio
async def test_chat_endpoint_task_query(client):
    """Test chat endpoint for task query"""
    response = await client.post(
        "/api/v1/chat",
        json={
            "input": "What tasks do I have due today?",
            "type": "text"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "details" in data

@pytest.mark.asyncio
async def test_chat_endpoint_audio_not_implemented(client):
    """Test chat endpoint with audio input (not implemented)"""
    response = await client.post(
        "/api/v1/chat",
        json={
            "input": "some_audio_content",
            "type": "audio"
        }
    )
    assert response.status_code == 400
    assert "not implemented" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_chat_endpoint_invalid_request(client):
    """Test chat endpoint with invalid request"""
    response = await client.post(
        "/api/v1/chat",
        json={
            "input": "Create a task",
            "type": "invalid_type"
        }
    )
    assert response.status_code == 422  # Validation error 