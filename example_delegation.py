"""
Example Usage of Cloud Agent Delegation

This example demonstrates how to delegate tasks to a cloud agent
for satellite connectivity operations.
"""

from src.cloud_agent import CloudAgentClient, DelegationService, CloudAgentConfig
from src.cloud_agent.delegation import TaskPriority


def main():
    """Example workflow for delegating tasks to cloud agent."""
    
    # Configure cloud agent connection
    config = CloudAgentConfig(
        endpoint="https://cloud-agent.example.com/api",
        api_key="your-api-key-here",
        timeout=30,
        max_retries=3
    )
    
    # Initialize client and delegation service
    client = CloudAgentClient(config)
    delegation_service = DelegationService(client)
    
    # Connect to cloud agent
    if client.connect():
        print("✓ Connected to cloud agent")
        
        # Delegate a satellite tracking task
        task_id = delegation_service.delegate_task(
            task_type="satellite_tracking",
            task_data={
                "satellite_id": "starlink-1234",
                "duration_minutes": 60,
                "tracking_mode": "continuous"
            },
            priority=TaskPriority.HIGH
        )
        print(f"✓ Task delegated with ID: {task_id}")
        
        # Delegate a signal analysis task
        task_id2 = delegation_service.delegate_task(
            task_type="signal_analysis",
            task_data={
                "frequency_range": [10.7, 12.7],
                "sample_rate": 1000000
            },
            priority=TaskPriority.MEDIUM
        )
        print(f"✓ Task delegated with ID: {task_id2}")
        
        # Check queue status
        queue_status = delegation_service.get_queue_status()
        print(f"\n✓ Tasks in queue: {len(queue_status)}")
        for task in queue_status:
            print(f"  - {task['task_type']} [{task['status']}]")
        
        # Disconnect when done
        client.disconnect()
        print("\n✓ Disconnected from cloud agent")
    else:
        print("✗ Failed to connect to cloud agent")


if __name__ == "__main__":
    main()
