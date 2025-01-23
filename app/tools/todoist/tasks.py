from typing import Optional, Dict, Any, List
from todoist_api_python.api import TodoistAPI


from app.core.config import get_settings
from app.core.logging import setup_logging

logger = setup_logging()
settings = get_settings()

class TodoistTools:
    def __init__(self):
        self.api = TodoistAPI(settings.TODOIST_API_KEY)
        
    async def create_task(self, 
                         title: str,
                         due_date: Optional[str] = None,
                         project_id: Optional[str] = None,
                         priority: Optional[int] = None) -> Dict[str, Any]:
        """Create a new task in Todoist"""
        try:
            task = self.api.add_task(
                content=title,
                due_string=due_date,
                project_id=project_id,
                priority=priority
            )
            logger.info(f"Created task: {task.id}")
            return {"success": True, "task_id": task.id, "content": task.content}
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return {"success": False, "error": str(e)}
            
    async def complete_task(self, task_id: str) -> Dict[str, bool]:
        """Mark a task as completed"""
        try:
            self.api.close_task(task_id=task_id)
            logger.info(f"Completed task: {task_id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error completing task: {str(e)}")
            return {"success": False, "error": str(e)}
            
    async def get_tasks(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all tasks, optionally filtered by project"""
        try:
            tasks = self.api.get_tasks(project_id=project_id)
            return [
                {
                    "id": task.id,
                    "content": task.content,
                    "due": task.due.date if task.due else None,
                    "priority": task.priority
                }
                for task in tasks
            ]
        except Exception as e:
            logger.error(f"Error getting tasks: {str(e)}")
            return []

    async def update_task(self, task_id: str, title: str = None, description: str = None, priority: int = None, due_date: str = None) -> dict:
        """Update a task in Todoist"""
        try:
            # Get the task first to ensure it exists
            task = self.api.get_task(task_id=task_id)
            
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["content"] = title
            if description is not None:
                update_data["description"] = description
            if priority is not None:
                update_data["priority"] = priority
            if due_date is not None:
                update_data["due_string"] = due_date
            
            # Update the task
            self.api.update_task(task_id=task_id, **update_data)
            logger.info(f"Updated task: {task_id}")
            
            return {"success": True, "task_id": task_id}
            
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            return {"success": False, "error": str(e)}

    async def reopen_task(self, task_id: str) -> Dict[str, bool]:
        """Reopen a completed task"""
        try:
            self.api.reopen_task(task_id=task_id)
            logger.info(f"Reopened task: {task_id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error reopening task: {str(e)}")
            return {"success": False, "error": str(e)}

    async def delete_task(self, task_id: str) -> Dict[str, bool]:
        """Delete a task from Todoist"""
        try:
            self.api.delete_task(task_id=task_id)
            logger.info(f"Deleted task: {task_id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects from Todoist"""
        try:
            projects = self.api.get_projects()
            return [
                {
                    "id": project.id,
                    "name": project.name,
                    "color": project.color,
                    "is_favorite": project.is_favorite,
                    "parent_id": project.parent_id,
                    "order": project.order
                }
                for project in projects
            ]
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}")
            return []

    async def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get all active (not completed) tasks"""
        try:
            tasks = self.api.get_tasks()
            return [
                {
                    "id": task.id,
                    "content": task.content,
                    "due": task.due.date if task.due else None,
                    "priority": task.priority,
                    "project_id": task.project_id,
                    "labels": task.labels,
                    "url": task.url
                }
                for task in tasks
            ]
        except Exception as e:
            logger.error(f"Error getting active tasks: {str(e)}")
            return []
