"""
Cloud Agent Delegation Module

This module provides functionality to delegate tasks to a cloud agent
for processing satellite connectivity operations.
"""

from .client import CloudAgentClient
from .delegation import DelegationService
from .config import CloudAgentConfig

__all__ = ['CloudAgentClient', 'DelegationService', 'CloudAgentConfig']
__version__ = '0.1.0'
