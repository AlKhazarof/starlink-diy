# Cloud Agent Delegation

This module provides functionality to delegate tasks to a cloud agent for processing satellite connectivity operations in the Starlink DIY project.

## Overview

The cloud agent delegation system allows you to offload compute-intensive or long-running tasks to a remote cloud agent via HTTP/HTTPS REST API, enabling:

- Satellite tracking and positioning calculations
- Signal analysis and processing
- Data aggregation and monitoring
- Remote diagnostics and troubleshooting

## Components

### CloudAgentConfig

Configuration class for cloud agent connection settings with validation.

```python
from src.cloud_agent import CloudAgentConfig

config = CloudAgentConfig(
    endpoint="https://cloud-agent.example.com/api",
    api_key="your-api-key",
    timeout=30,        # Request timeout in seconds (must be > 0)
    max_retries=3      # Number of retries on failure (must be >= 0)
)
```

**Configuration Parameters:**
- `endpoint` (required): Cloud agent API endpoint URL. Must be a non-empty string.
- `api_key` (optional): API key for authentication. Sent as Bearer token in Authorization header.
- `timeout` (default: 30): HTTP request timeout in seconds. Must be positive.
- `max_retries` (default: 3): Maximum number of retry attempts on failure. Must be non-negative.

### CloudAgentClient

HTTP/HTTPS client for communicating with cloud agents using the requests library.

**Features:**
- Real HTTP/HTTPS communication via REST API
- Automatic retry with exponential backoff on server errors (429, 500, 502, 503, 504)
- Bearer token authentication via Authorization header
- Configurable timeouts
- Connection lifecycle management

```python
from src.cloud_agent import CloudAgentClient

client = CloudAgentClient(config)

# Connect to cloud agent (tests /health endpoint)
if client.connect():
    # Send a task (POST /tasks)
    response = client.send_task("satellite_tracking", {
        "satellite_id": "starlink-1234",
        "duration_minutes": 60
    })
    print(f"Task ID: {response['task_id']}")
    
    # Check task status (GET /tasks/{task_id})
    status = client.get_task_status(response['task_id'])
    print(f"Status: {status['status']}")
    
    # Disconnect when done
    client.disconnect()
```

**API Endpoints:**
- `GET /health` - Health check endpoint for connection testing
- `POST /tasks` - Submit a new task for processing
- `GET /tasks/{task_id}` - Get status of a specific task

**Error Handling:**
- `ConnectionError`: Raised when operations are attempted without connection
- `ValueError`: Raised for invalid input parameters
- `requests.exceptions.RequestException`: Raised on HTTP errors

**Retry Logic:**
- Exponential backoff: 1s, 2s, 4s, 8s... between retries
- Automatic retry on server errors (5xx) and rate limiting (429)
- Configurable maximum retry attempts via `max_retries` config parameter

### DelegationService

High-level service for managing task delegation and queue with status refresh capabilities.

```python
from src.cloud_agent import DelegationService
from src.cloud_agent.delegation import TaskPriority

service = DelegationService(client)

# Delegate a task with priority
task_id = service.delegate_task(
    task_type="signal_analysis",
    task_data={"frequency_range": [10.7, 12.7]},
    priority=TaskPriority.HIGH
)

# Check queue status
queue = service.get_queue_status()

# Refresh status of specific task from cloud agent
status = service.refresh_task_status(task_id)
print(f"Updated status: {status['status']}")

# Refresh all task statuses
all_statuses = service.refresh_all_statuses()

# Clear completed, failed, and cancelled tasks
removed = service.clear_completed_tasks()
print(f"Removed {removed} task(s)")
```

**Input Validation:**
- `task_type`: Must be a non-empty string
- `task_data`: Must be a dictionary
- Raises `ValueError` for invalid inputs

## Task Types

Common task types for satellite connectivity:

- `satellite_tracking` - Track satellite positions and predict passes
- `signal_analysis` - Analyze signal strength and quality
- `frequency_scan` - Scan frequency ranges for signals
- `data_processing` - Process collected telemetry data
- `diagnostics` - Run diagnostic checks on equipment

## Priority Levels

Tasks can be assigned priority levels:

- `TaskPriority.LOW` - Background tasks
- `TaskPriority.MEDIUM` - Normal operations (default)
- `TaskPriority.HIGH` - Important time-sensitive tasks
- `TaskPriority.CRITICAL` - Urgent tasks requiring immediate attention

## Example Usage

See `example_delegation.py` for a complete working example:

```bash
# Set API key as environment variable (recommended)
export CLOUD_AGENT_API_KEY="your-api-key-here"

# Run example
python example_delegation.py
```

The example demonstrates:
- Connecting to cloud agent
- Delegating two tasks with different priorities
- Checking initial queue status
- Refreshing task statuses
- Clearing completed tasks

## Security Considerations

### API Key Management
1. **Environment Variables**: Store API keys in environment variables, never in code
   ```bash
   export CLOUD_AGENT_API_KEY="your-key-here"
   api_key = os.environ.get('CLOUD_AGENT_API_KEY')
   ```
2. **Never Commit Secrets**: Add API keys to `.gitignore`
3. **Rotate Keys**: Regularly rotate API keys
4. **Least Privilege**: Use keys with minimum required permissions

### Network Security
1. **Use HTTPS**: Always use HTTPS endpoints, never plain HTTP
2. **TLS/SSL**: Ensure TLS 1.2 or higher
3. **Certificate Validation**: Don't disable SSL verification

### Timeouts and Rate Limiting
1. **Set Timeouts**: Always configure reasonable timeout values (e.g., 30 seconds)
2. **Limit Retries**: Set max_retries to prevent infinite loops (e.g., 3 retries)
3. **Backoff Strategy**: Exponential backoff prevents overwhelming the server
4. **Handle 429**: Respect rate limit responses from server

### Data Privacy
1. **Minimize Data**: Only send necessary data to cloud agent
2. **Sensitive Data**: Avoid sending personal or sensitive information
3. **Audit Logs**: Monitor what data is being sent

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

Test coverage includes:
- Configuration validation
- HTTP client behavior (mocked)
- Retry and backoff logic
- Authentication headers
- Status refresh operations
- Input validation
- Error handling

## Requirements

Install required dependencies:

```bash
pip install requests>=2.31.0
```

The client uses:
- `requests` - HTTP library
- `urllib3.util.retry.Retry` - Retry logic with exponential backoff
- `requests.adapters.HTTPAdapter` - Custom retry configuration

## Architecture

```
┌─────────────────┐
│ Your Application│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│DelegationService│ ◄── Task Queue Management
└────────┬────────┘     Status Refresh
         │
         ▼
┌─────────────────┐
│CloudAgentClient │ ◄── HTTP/HTTPS Communication
└────────┬────────┘     Retry Logic + Auth
         │
         ▼
┌─────────────────┐
│   Cloud Agent   │ ◄── REST API
│   (Remote)      │     /health, /tasks
└─────────────────┘
```

## Future Enhancements

- Async task execution with asyncio
- Task result caching
- WebSocket support for real-time updates
- Task cancellation and timeout handling
- Batch task submission
- Streaming responses for large results
- Metrics and monitoring integration
