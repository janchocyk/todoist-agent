import pytest
from app.tools.todoist.tasks import TodoistTools

@pytest.mark.asyncio
async def test_create_task(todoist_tools: TodoistTools, test_task_data: dict):
    """Test task creation"""
    result = await todoist_tools.create_task(
        title=test_task_data["title"],
        due_date=test_task_data["due_date"],
        priority=test_task_data["priority"]
    )
    assert result["success"] is True
    assert "task_id" in result
    return result["task_id"]

@pytest.mark.asyncio
async def test_get_tasks(todoist_tools: TodoistTools):
    """Test getting tasks"""
    tasks = await todoist_tools.get_tasks()
    assert isinstance(tasks, list)
    if tasks:  # Only check if there are tasks
        for task in tasks:
            assert "id" in task
            assert "content" in task

@pytest.mark.asyncio
async def test_update_task(todoist_tools: TodoistTools, test_task_data: dict):
    """Test task update"""
    # First create a task
    task_id = await test_create_task(todoist_tools, test_task_data)
    
    # Update the task
    new_title = "Updated Test Task"
    update_result = await todoist_tools.update_task(
        task_id=task_id,
        title=new_title,
        priority=2
    )
    assert update_result["success"] is True
    
    # Verify the update by getting the task
    tasks = await todoist_tools.get_tasks()
    updated_task = next((task for task in tasks if task["id"] == task_id), None)
    assert updated_task is not None
    assert updated_task["content"] == new_title

@pytest.mark.asyncio
async def test_complete_and_reopen_task(todoist_tools: TodoistTools, test_task_data: dict):
    """Test task completion and reopening"""
    # First create a task
    task_id = await test_create_task(todoist_tools, test_task_data)
    
    # Complete the task
    complete_result = await todoist_tools.complete_task(task_id)
    assert complete_result["success"] is True
    
    # Reopen the task
    reopen_result = await todoist_tools.reopen_task(task_id)
    assert reopen_result["success"] is True

@pytest.mark.asyncio
async def test_delete_task(todoist_tools: TodoistTools, test_task_data: dict):
    """Test task deletion"""
    # First create a task
    task_id = await test_create_task(todoist_tools, test_task_data)
    
    # Delete the task
    delete_result = await todoist_tools.delete_task(task_id)
    assert delete_result["success"] is True 