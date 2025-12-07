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
            ValueError: If task_type is empty or task_data is not a dict
        """
        if not self.client.is_connected():
            raise ConnectionError("Client not connected to cloud agent")
        
        # Validate inputs
        if not task_type or not isinstance(task_type, str):
            raise ValueError("task_type must be a non-empty string")
        if not isinstance(task_data, dict):
            raise ValueError("task_data must be a dictionary")
        
        # Add priority to task data
        enriched_data = {
            **task_data,
            'priority': priority.value
        }
        
        # Submit task through client
        response = self.client.send_task(task_type, enriched_data)
        
        # Track task in queue
        task_id = response.get('task_id')
        self.task_queue.append({
            'task_id': task_id,
            'task_type': task_type,
            'priority': priority,
            'status': response.get('status', 'unknown')
        })
        
        return task_id
    
    def get_queue_status(self) -> List[Dict[str, Any]]:
        """
        Get status of all tasks in queue.
        
        Returns:
            list: List of task status information
        """
        return self.task_queue.copy()
    
    def refresh_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Refresh status of a specific task from the cloud agent.
        
        Args:
            task_id: ID of the task to refresh
            
        Returns:
            dict: Updated task status information
            
        Raises:
            ConnectionError: If client not connected
            ValueError: If task_id not found in queue
        """
        if not self.client.is_connected():
            raise ConnectionError("Client not connected to cloud agent")
        
        # Find task in queue
        task_index = None
        for i, task in enumerate(self.task_queue):
            if task['task_id'] == task_id:
                task_index = i
                break
        
        if task_index is None:
            raise ValueError(f"Task {task_id} not found in queue")
        
        # Get updated status from cloud agent
        status_response = self.client.get_task_status(task_id)
        
        # Update task in queue
        self.task_queue[task_index]['status'] = status_response.get('status', 'unknown')
        
        return status_response
    
    def refresh_all_statuses(self) -> List[Dict[str, Any]]:
        """
        Refresh status of all tasks in queue from the cloud agent.
        
        Returns:
            list: List of updated task status information
            
        Raises:
            ConnectionError: If client not connected
        """
        if not self.client.is_connected():
            raise ConnectionError("Client not connected to cloud agent")
        
        updated_statuses = []
        for task in self.task_queue:
            try:
                status = self.refresh_task_status(task['task_id'])
                updated_statuses.append(status)
            except (ConnectionError, ValueError, Exception) as e:
                # Skip tasks that fail to refresh due to connection, validation, or HTTP errors
                # Log error but continue processing other tasks
                continue
        
        return updated_statuses
    
    def clear_completed_tasks(self) -> int:
        """
        Remove completed, failed, and cancelled tasks from queue.
        
        This clears tasks that have finished processing, regardless of
        whether they succeeded or failed.
        
        Returns:
            int: Number of tasks removed
        """
        initial_count = len(self.task_queue)
        self.task_queue = [
            task for task in self.task_queue 
            if task['status'] not in ('completed', 'failed', 'cancelled')
        ]
        return initial_count - len(self.task_queue)
