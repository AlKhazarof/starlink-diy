"""
Cloud Agent Configuration Module

Handles configuration for cloud agent connections and delegation settings.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CloudAgentConfig:
    """Configuration for cloud agent connection."""
    
    endpoint: str
    api_key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    
    def __post_init__(self):
        """Validate configuration parameters."""
        if not self.endpoint:
            raise ValueError("Endpoint must be provided")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
