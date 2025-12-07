"""
Tests for Cloud Agent Delegation Module
"""

import unittest
from src.cloud_agent import CloudAgentClient, DelegationService, CloudAgentConfig
from src.cloud_agent.delegation import TaskPriority


class TestCloudAgentConfig(unittest.TestCase):
    """Test cases for CloudAgentConfig."""
    
    def test_valid_config(self):
        """Test creating valid configuration."""
        config = CloudAgentConfig(
            endpoint="https://example.com",
            api_key="test-key",
            timeout=30,
            max_retries=3
        )
        self.assertEqual(config.endpoint, "https://example.com")
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.max_retries, 3)
    
    def test_empty_endpoint(self):
        """Test that empty endpoint raises ValueError."""
        with self.assertRaises(ValueError):
            CloudAgentConfig(endpoint="")
    
    def test_invalid_timeout(self):
        """Test that invalid timeout raises ValueError."""
        with self.assertRaises(ValueError):
            CloudAgentConfig(endpoint="https://example.com", timeout=0)
    
    def test_invalid_retries(self):
        """Test that negative retries raises ValueError."""
        with self.assertRaises(ValueError):
            CloudAgentConfig(endpoint="https://example.com", max_retries=-1)


class TestCloudAgentClient(unittest.TestCase):
    """Test cases for CloudAgentClient."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = CloudAgentConfig(endpoint="https://test.example.com")
        self.client = CloudAgentClient(self.config)
    
    def test_initial_state(self):
        """Test client initial state."""
        self.assertFalse(self.client.is_connected())
    
    def test_connect(self):
        """Test connection to cloud agent."""
        result = self.client.connect()
        self.assertTrue(result)
        self.assertTrue(self.client.is_connected())
    
    def test_disconnect(self):
        """Test disconnection from cloud agent."""
        self.client.connect()
        self.client.disconnect()
        self.assertFalse(self.client.is_connected())
    
    def test_send_task_not_connected(self):
        """Test sending task when not connected raises error."""
        with self.assertRaises(ConnectionError):
            self.client.send_task("test_task", {})
    
    def test_send_task_connected(self):
        """Test sending task when connected."""
        self.client.connect()
        response = self.client.send_task("test_task", {"data": "test"})
        self.assertEqual(response['status'], 'submitted')
        self.assertEqual(response['task_type'], 'test_task')
    
    def test_get_task_status_not_connected(self):
        """Test getting task status when not connected raises error."""
        with self.assertRaises(ConnectionError):
            self.client.get_task_status("test-id")


class TestDelegationService(unittest.TestCase):
    """Test cases for DelegationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        config = CloudAgentConfig(endpoint="https://test.example.com")
        self.client = CloudAgentClient(config)
        self.service = DelegationService(self.client)
    
    def test_delegate_task_not_connected(self):
        """Test delegating task when not connected raises error."""
        with self.assertRaises(ConnectionError):
            self.service.delegate_task("test_task", {})
    
    def test_delegate_task_connected(self):
        """Test delegating task when connected."""
        self.client.connect()
        task_id = self.service.delegate_task(
            "test_task",
            {"data": "test"},
            TaskPriority.HIGH
        )
        self.assertIsNotNone(task_id)
        self.assertEqual(len(self.service.task_queue), 1)
    
    def test_get_queue_status(self):
        """Test getting queue status."""
        self.client.connect()
        self.service.delegate_task("task1", {})
        self.service.delegate_task("task2", {})
        
        queue_status = self.service.get_queue_status()
        self.assertEqual(len(queue_status), 2)
    
    def test_clear_completed_tasks(self):
        """Test clearing completed tasks."""
        self.client.connect()
        self.service.delegate_task("task1", {})
        
        # Manually mark task as completed for testing
        self.service.task_queue[0]['status'] = 'completed'
        
        removed = self.service.clear_completed_tasks()
        self.assertEqual(removed, 1)
        self.assertEqual(len(self.service.task_queue), 0)


if __name__ == '__main__':
    unittest.main()
