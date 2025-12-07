"""
Example Usage of Cloud Agent Delegation

This example demonstrates how to delegate tasks to a cloud agent
for satellite connectivity operations.
"""

import os
import time
from src.cloud_agent import CloudAgentClient, DelegationService, CloudAgentConfig
from src.cloud_agent.delegation import TaskPriority


def main():
    """Example workflow for delegating tasks to cloud agent."""
    
    # Configure cloud agent connection
    # API key should be stored in environment variable for security
    api_key = os.environ.get('CLOUD_AGENT_API_KEY', 'your-api-key-here')
    
    config = CloudAgentConfig(
        endpoint="https://cloud-agent.example.com/api",
        api_key=api_key,
        timeout=30,
        max_retries=3
    )
    
    # Initialize client and delegation service
    client = CloudAgentClient(config)
    delegation_service = DelegationService(client)
    
    # Connect to cloud agent
    print("Connecting to cloud agent...")
    if client.connect():
        print("✓ Connected to cloud agent")
        
        try:
            # Delegate a satellite tracking task
            print("\nDelegating satellite tracking task...")
            task_id1 = delegation_service.delegate_task(
                task_type="satellite_tracking",
                task_data={
                    "satellite_id": "starlink-1234",
                    "duration_minutes": 60,
                    "tracking_mode": "continuous"
                },
                priority=TaskPriority.HIGH
            )
            print(f"✓ Task delegated with ID: {task_id1}")
            
            # Delegate a signal analysis task
            print("\nDelegating signal analysis task...")
            task_id2 = delegation_service.delegate_task(
                task_type="signal_analysis",
                task_data={
                    "frequency_range": [10.7, 12.7],
                    "sample_rate": 1000000
                },
                priority=TaskPriority.MEDIUM
            )
            print(f"✓ Task delegated with ID: {task_id2}")
            
            # Check initial queue status
            queue_status = delegation_service.get_queue_status()
            print(f"\n✓ Initial queue status: {len(queue_status)} tasks")
            for task in queue_status:
                print(f"  - {task['task_type']} (ID: {task['task_id']}) [{task['status']}]")
            
            # Simulate waiting for tasks to process
            print("\nWaiting for tasks to process...")
            time.sleep(2)
            
            # Refresh status of first task
            print(f"\nRefreshing status for task {task_id1}...")
            status1 = delegation_service.refresh_task_status(task_id1)
            print(f"✓ Task {task_id1} status: {status1.get('status')}")
            
            # Refresh status of second task
            print(f"\nRefreshing status for task {task_id2}...")
            status2 = delegation_service.refresh_task_status(task_id2)
            print(f"✓ Task {task_id2} status: {status2.get('status')}")
            
            # Get updated queue status
            queue_status = delegation_service.get_queue_status()
            print(f"\n✓ Updated queue status: {len(queue_status)} tasks")
            for task in queue_status:
                print(f"  - {task['task_type']} (ID: {task['task_id']}) [{task['status']}]")
            
            # Clear completed/failed tasks
            removed = delegation_service.clear_completed_tasks()
            if removed > 0:
                print(f"\n✓ Cleared {removed} completed/failed task(s)")
            
            # Final queue status
            queue_status = delegation_service.get_queue_status()
            print(f"\n✓ Final queue status: {len(queue_status)} task(s) remaining")
            
        except Exception as e:
            print(f"\n✗ Error during task delegation: {e}")
        finally:
            # Disconnect when done
            client.disconnect()
            print("\n✓ Disconnected from cloud agent")
    else:
        print("✗ Failed to connect to cloud agent")
        print("  Make sure the cloud agent endpoint is accessible")
        print("  and your API key is valid (set CLOUD_AGENT_API_KEY env var)")


if __name__ == "__main__":
    main()
