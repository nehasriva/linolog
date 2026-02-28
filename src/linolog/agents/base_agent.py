from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class BaseAgent(ABC):
    """Base class for all agents in the LinoLog system."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        """
        Process metadata and return updated metadata.
        
        Args:
            metadata: Current metadata dictionary
            folder_path: Path to the print folder
            
        Returns:
            Updated metadata dictionary
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if this agent is enabled in configuration."""
        from linolog.config import Config
        agent_name = self.__class__.__name__.lower()
        
        if hasattr(Config, f'ENABLE_{agent_name.upper()}'):
            return getattr(Config, f'ENABLE_{agent_name.upper()}')
        
        return True  # Default to enabled if not specified 