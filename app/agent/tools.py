# from langchain_core.tools import tool
from typing import Optional, Dict, Any, List

from app.tools.todoist.tasks import TodoistTools

todoist = TodoistTools()

async def create_todoist_task(
    title: str,
    due_date: Optional[str] = None,
    project_id: Optional[str] = None,
    priority: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new task in Todoist.
    Args:
        title: The task title/content
        due_date: Optional due date (e.g. 'tomorrow', 'next monday')
        project_id: Optional project ID to add task to
        priority: Optional priority level (1-4)
    """
    return await todoist.create_task(title, due_date, project_id, priority)

async def complete_todoist_task(task_id: str) -> Dict[str, bool]:
    """Mark a Todoist task as completed. Other word task finished.
    Args:
        task_id: The ID of the task to complete
    """
    return await todoist.complete_task(task_id)


async def get_todoist_tasks(project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all Todoist tasks, optionally filtered by project.
    Args:
        project_id: Optional project ID to filter tasks
    """
    return await todoist.get_tasks(project_id)


async def update_todoist_task(
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[int] = None,
    due_date: Optional[str] = None
) -> Dict[str, Any]:
    """Update an existing Todoist task.
    Args:
        task_id: The ID of the task to update
        title: Optional new title for the task
        priority: Optional new priority (1-4)
        due_date: Optional new due date
    """
    return await todoist.update_task(task_id, title, description, priority, due_date)


async def reopen_todoist_task(task_id: str) -> Dict[str, bool]:
    """Reopen a completed Todoist task.
    Args:
        task_id: The ID of the task to reopen
    """
    return await todoist.reopen_task(task_id)


async def delete_todoist_task(task_id: str) -> Dict[str, bool]:
    """Delete a Todoist task. Not to be confused with the task of theisaccomplished.
    Args:
        task_id: The ID of the task to delete
    """
    return await todoist.delete_task(task_id)


async def get_todoist_projects() -> List[Dict[str, Any]]:
    """Get all Todoist projects."""
    return await todoist.get_projects()


async def get_active_todoist_tasks() -> List[Dict[str, Any]]:
    """Get all active (not completed) Todoist tasks."""
    return await todoist.get_active_tasks()

def get_tools():
    return {
        "create_todoist_task": create_todoist_task,
        "complete_todoist_task": complete_todoist_task,
        "get_todoist_tasks": get_todoist_tasks,
        "update_todoist_task": update_todoist_task,
        "reopen_todoist_task": reopen_todoist_task,
        "delete_todoist_task": delete_todoist_task,
        "get_todoist_projects": get_todoist_projects,
        "get_active_todoist_tasks": get_active_todoist_tasks
    }