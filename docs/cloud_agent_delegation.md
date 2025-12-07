# Cloud Agent Delegation

This module provides functionality to delegate tasks to a cloud agent for processing satellite connectivity operations in the Starlink DIY project.

## Overview

The cloud agent delegation system allows you to offload compute-intensive or long-running tasks to a remote cloud agent, enabling:

- Satellite tracking and positioning calculations
- Signal analysis and processing
- Data aggregation and monitoring
- Remote diagnostics and troubleshooting

## Components

### CloudAgentConfig

Configuration class for cloud agent connection settings.

```python
from src.cloud_agent import CloudAgentConfig

config = CloudAgentConfig(
    endpoint="https://cloud-agent.example.com/api",
    api_key="your-api-key",
    timeout=30,
    max_retries=3
)
```

### CloudAgentClient

Client interface for communicating with cloud agents.

```python
from src.cloud_agent import CloudAgentClient

client = CloudAgentClient(config)
client.connect()

# Send a task
response = client.send_task("satellite_tracking", {
    "satellite_id": "starlink-1234",
    "duration_minutes": 60
})

# Check task status
status = client.get_task_status(response['task_id'])
```

### DelegationService

High-level service for managing task delegation and queue.

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
```

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
python example_delegation.py
```

## Security Considerations

1. **API Keys**: Always use environment variables or secure key management for API keys
2. **Encryption**: Ensure all communication uses HTTPS/TLS
3. **Authentication**: Implement proper authentication mechanisms
4. **Data Privacy**: Be mindful of what data is sent to cloud agents

## Testing

Run the test suite:

```bash
python -m unittest tests/test_cloud_agent.py
```

## Future Enhancements

- Real HTTP/HTTPS client implementation
- Async task execution
- Task result caching
- Retry mechanisms with exponential backoff
- WebSocket support for real-time updates
- Task cancellation and timeout handling
