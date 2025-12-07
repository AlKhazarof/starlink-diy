"""
Cloud Agent Client Module

Provides client interface for communicating with cloud agents.
"""

from typing import Dict, Any, Optional
import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class CloudAgentClient:
    """Client for interacting with cloud agents via HTTP/HTTPS."""
    
    def __init__(self, config):
        """
        Initialize cloud agent client.
        
        Args:
            config: CloudAgentConfig instance with connection settings
        """
        self.config = config
        self._connected = False
        self._session = None
    
    def connect(self) -> bool:
        """
        Establish connection to cloud agent.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create session with retry strategy
            self._session = requests.Session()
            
            # Configure retry strategy with exponential backoff
            retry_strategy = Retry(
                total=self.config.max_retries,
                backoff_factor=1,  # Wait 1, 2, 4, 8... seconds
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
            )
            
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)
            
            # Set headers if API key provided
            if self.config.api_key:
                self._session.headers.update({
                    'Authorization': f'Bearer {self.config.api_key}',
                    'Content-Type': 'application/json'
                })
            
            # Test connection with health check
            response = self._session.get(
                f"{self.config.endpoint}/health",
                timeout=self.config.timeout
            )
            
            self._connected = response.status_code == 200
            return self._connected
            
        except requests.exceptions.RequestException:
            # Connection failed, but don't raise - return False
            self._connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from cloud agent."""
        if self._session:
            self._session.close()
            self._session = None
        self._connected = False
    
    def is_connected(self) -> bool:
        """Check if client is connected to cloud agent."""
        return self._connected
    
    def send_task(self, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a task to the cloud agent for processing.
        
        Args:
            task_type: Type of task to delegate
            task_data: Task-specific data
            
        Returns:
            dict: Response from cloud agent containing task result
            
        Raises:
            ConnectionError: If not connected to cloud agent
            ValueError: If task_type is empty or task_data is not a dict
            requests.exceptions.RequestException: If HTTP request fails
        """
        if not self._connected or not self._session:
            raise ConnectionError("Not connected to cloud agent")
        
        # Validate inputs
        if not task_type or not isinstance(task_type, str):
            raise ValueError("task_type must be a non-empty string")
        if not isinstance(task_data, dict):
            raise ValueError("task_data must be a dictionary")
        
        # Prepare task payload
        payload = {
            'task_type': task_type,
            'task_data': task_data
        }
        
        # Send task to cloud agent
        response = self._session.post(
            f"{self.config.endpoint}/tasks",
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get status of a delegated task.
        
        Args:
            task_id: ID of the task to check
            
        Returns:
            dict: Task status information
            
        Raises:
            ConnectionError: If not connected to cloud agent
            ValueError: If task_id is empty
            requests.exceptions.RequestException: If HTTP request fails
        """
        if not self._connected or not self._session:
            raise ConnectionError("Not connected to cloud agent")
        
        # Validate input
        if not task_id or not isinstance(task_id, str):
            raise ValueError("task_id must be a non-empty string")
        
        # Query task status
        response = self._session.get(
            f"{self.config.endpoint}/tasks/{task_id}",
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        return response.json()
