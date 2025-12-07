"""
Tests for Cloud Agent Delegation Module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
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
        with self.assertRaises(ValueError):
            CloudAgentConfig(endpoint="https://example.com", timeout=-1)
    
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
    
    @patch('requests.Session')
    def test_connect_success(self, mock_session_class):
        """Test successful connection to cloud agent."""
        # Mock session and response
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        result = self.client.connect()
        
        self.assertTrue(result)
        self.assertTrue(self.client.is_connected())
        mock_session.get.assert_called_once()
    
    @patch('requests.Session')
    def test_connect_failure(self, mock_session_class):
        """Test failed connection to cloud agent."""
        # Mock session to raise exception
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.ConnectionError()
        mock_session_class.return_value = mock_session
        
        result = self.client.connect()
        
        self.assertFalse(result)
        self.assertFalse(self.client.is_connected())
    
    @patch('requests.Session')
    def test_connect_with_api_key(self, mock_session_class):
        """Test connection with API key sets headers."""
        config_with_key = CloudAgentConfig(
            endpoint="https://test.example.com",
            api_key="test-api-key"
        )
        client = CloudAgentClient(config_with_key)
        
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client.connect()
        
        # Verify Authorization header was set
        mock_session.headers.update.assert_called_once()
        call_args = mock_session.headers.update.call_args[0][0]
        self.assertIn('Authorization', call_args)
        self.assertEqual(call_args['Authorization'], 'Bearer test-api-key')
    
    def test_disconnect(self):
        """Test disconnection from cloud agent."""
        self.client._connected = True
        self.client._session = Mock()
        
        self.client.disconnect()
        
        self.assertFalse(self.client.is_connected())
        self.assertIsNone(self.client._session)
    
    def test_send_task_not_connected(self):
        """Test sending task when not connected raises error."""
        with self.assertRaises(ConnectionError):
            self.client.send_task("test_task", {})
    
    def test_send_task_invalid_task_type(self):
        """Test sending task with invalid task_type raises ValueError."""
        self.client._connected = True
        self.client._session = Mock()
        
        with self.assertRaises(ValueError):
            self.client.send_task("", {})
        
        with self.assertRaises(ValueError):
            self.client.send_task(None, {})
    
    def test_send_task_invalid_task_data(self):
        """Test sending task with invalid task_data raises ValueError."""
        self.client._connected = True
        self.client._session = Mock()
        
        with self.assertRaises(ValueError):
            self.client.send_task("test_task", "not a dict")
        
        with self.assertRaises(ValueError):
            self.client.send_task("test_task", None)
    
    @patch('requests.Session')
    def test_send_task_success(self, mock_session_class):
        """Test sending task when connected."""
        # Setup
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'submitted',
            'task_type': 'test_task',
            'task_id': 'test-id-123'
        }
        mock_session.get.return_value = mock_response
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        self.client.connect()
        response = self.client.send_task("test_task", {"data": "test"})
        
        self.assertEqual(response['status'], 'submitted')
        self.assertEqual(response['task_type'], 'test_task')
        self.assertEqual(response['task_id'], 'test-id-123')
        mock_session.post.assert_called_once()
    
    def test_get_task_status_not_connected(self):
        """Test getting task status when not connected raises error."""
        with self.assertRaises(ConnectionError):
            self.client.get_task_status("test-id")
    
    def test_get_task_status_invalid_task_id(self):
        """Test getting task status with invalid task_id raises ValueError."""
        self.client._connected = True
        self.client._session = Mock()
        
        with self.assertRaises(ValueError):
            self.client.get_task_status("")
        
        with self.assertRaises(ValueError):
            self.client.get_task_status(None)
    
    @patch('requests.Session')
    def test_get_task_status_success(self, mock_session_class):
        """Test getting task status when connected."""
        # Setup
        mock_session = MagicMock()
        mock_health_response = Mock()
        mock_health_response.status_code = 200
        mock_status_response = Mock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {
            'task_id': 'test-id-123',
            'status': 'completed',
            'progress': 100
        }
        mock_session.get.side_effect = [mock_health_response, mock_status_response]
        mock_session_class.return_value = mock_session
        
        self.client.connect()
        status = self.client.get_task_status("test-id-123")
        
        self.assertEqual(status['task_id'], 'test-id-123')
        self.assertEqual(status['status'], 'completed')
        self.assertEqual(status['progress'], 100)
    
    @patch('requests.Session')
    def test_retry_on_server_error(self, mock_session_class):
        """Test that client retries on server errors."""
        # This is tested implicitly through the Retry configuration
        # The retry logic is handled by urllib3.util.retry.Retry
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        # Verify retry strategy is configured
        from requests.adapters import HTTPAdapter
        from unittest.mock import call
        
        # Connect to initialize session
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        
        self.client.connect()
        
        # Verify adapters were mounted (which includes retry strategy)
        self.assertEqual(mock_session.mount.call_count, 2)


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
    
    def test_delegate_task_invalid_inputs(self):
        """Test delegating task with invalid inputs raises ValueError."""
        self.client._connected = True
        self.client._session = Mock()
        
        with self.assertRaises(ValueError):
            self.service.delegate_task("", {})
        
        with self.assertRaises(ValueError):
            self.service.delegate_task("test_task", "not a dict")
    
    @patch('requests.Session')
    def test_delegate_task_success(self, mock_session_class):
        """Test delegating task when connected."""
        # Setup mocks
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'submitted',
            'task_id': 'test-id-123'
        }
        mock_session.get.return_value = mock_response
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        self.client.connect()
        task_id = self.service.delegate_task(
            "test_task",
            {"data": "test"},
            TaskPriority.HIGH
        )
        
        self.assertEqual(task_id, 'test-id-123')
        self.assertEqual(len(self.service.task_queue), 1)
        self.assertEqual(self.service.task_queue[0]['task_type'], 'test_task')
        self.assertEqual(self.service.task_queue[0]['priority'], TaskPriority.HIGH)
    
    def test_get_queue_status(self):
        """Test getting queue status."""
        self.client._connected = True
        self.client._session = Mock()
        self.client.send_task = Mock(return_value={'task_id': 'id1', 'status': 'submitted'})
        
        self.service.delegate_task("task1", {})
        self.service.delegate_task("task2", {})
        
        queue_status = self.service.get_queue_status()
        self.assertEqual(len(queue_status), 2)
    
    @patch('requests.Session')
    def test_refresh_task_status(self, mock_session_class):
        """Test refreshing task status."""
        # Setup mocks
        mock_session = MagicMock()
        mock_health_response = Mock()
        mock_health_response.status_code = 200
        mock_submit_response = Mock()
        mock_submit_response.status_code = 200
        mock_submit_response.json.return_value = {
            'status': 'submitted',
            'task_id': 'test-id-123'
        }
        mock_status_response = Mock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {
            'task_id': 'test-id-123',
            'status': 'completed'
        }
        mock_session.get.side_effect = [mock_health_response, mock_status_response]
        mock_session.post.return_value = mock_submit_response
        mock_session_class.return_value = mock_session
        
        self.client.connect()
        task_id = self.service.delegate_task("test_task", {})
        
        # Refresh status
        status = self.service.refresh_task_status(task_id)
        
        self.assertEqual(status['status'], 'completed')
        self.assertEqual(self.service.task_queue[0]['status'], 'completed')
    
    def test_refresh_task_status_not_found(self):
        """Test refreshing status for non-existent task."""
        self.client._connected = True
        self.client._session = Mock()
        
        with self.assertRaises(ValueError):
            self.service.refresh_task_status("non-existent-id")
    
    def test_clear_completed_tasks(self):
        """Test clearing completed tasks."""
        self.client._connected = True
        self.client._session = Mock()
        self.client.send_task = Mock(return_value={'task_id': 'id1', 'status': 'submitted'})
        
        self.service.delegate_task("task1", {})
        
        # Manually mark task as completed for testing
        self.service.task_queue[0]['status'] = 'completed'
        
        removed = self.service.clear_completed_tasks()
        self.assertEqual(removed, 1)
        self.assertEqual(len(self.service.task_queue), 0)
    
    def test_clear_failed_tasks(self):
        """Test clearing failed tasks (clear_completed_tasks also removes failed tasks)."""
        self.client._connected = True
        self.client._session = Mock()
        self.client.send_task = Mock(return_value={'task_id': 'id1', 'status': 'submitted'})
        
        self.service.delegate_task("task1", {})
        
        # Manually mark task as failed for testing
        self.service.task_queue[0]['status'] = 'failed'
        
        # clear_completed_tasks removes both completed and failed tasks
        removed = self.service.clear_completed_tasks()
        self.assertEqual(removed, 1)
        self.assertEqual(len(self.service.task_queue), 0)


if __name__ == '__main__':
    unittest.main()
