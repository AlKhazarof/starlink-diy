"""
Delegation Service Module

Handles task delegation logic and routing to cloud agents.
"""

from typing import Dict, Any, List, Optional
from enum import Enum


class TaskPriority(Enum):
    """Priority levels for delegated tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class DelegationService:
    """Service for managing task delegation to cloud agents."""
    
    def __init__(self, client):
        """
        Initialize delegation service.
        
        Args:
            client: CloudAgentClient instance for communication
        """
        self.client = client
        self.task_queue: List[Dict[str, Any]] = []
    
    def delegate_task(
        self, 
        task_type: str, 
        task_data: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> str:
        """
        Delegate a task to the cloud agent.
        
        Args:
            task_type: Type of task to delegate
            task_data: Task-specific data
            priority: Task priority level
            
        Returns:
            str: Task ID for tracking
            
        Raises:
            ConnectionError: If client not connected
        """
        if not self.client.is_connected():
            raise ConnectionError("Client not connected to cloud agent")
        
        # Add priority to task data
        enriched_data = {
            **task_data,
            'priority': priority.value
        }
        
        # Submit task through client
        response = self.client.send_task(task_type, enriched_data)
        
        # Track task in queue
        self.task_queue.append({
            'task_id': response.get('task_id'),
            'task_type': task_type,
            'priority': priority,
            'status': response.get('status')
        })
        
        return response.get('task_id')
    
    def get_queue_status(self) -> List[Dict[str, Any]]:
        """
        Get status of all tasks in queue.
        
        Returns:
            list: List of task status information
        """
        return self.task_queue.copy()
    
    def clear_completed_tasks(self) -> int:
        """
        Remove completed tasks from queue.
        
        Returns:
            int: Number of tasks removed
        """
        initial_count = len(self.task_queue)
        self.task_queue = [
            task for task in self.task_queue 
            if task['status'] not in ('completed', 'failed')
        ]
        return initial_count - len(self.task_queue)
