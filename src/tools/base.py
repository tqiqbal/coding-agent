"""Base tool infrastructure for the AI assistant."""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

class Tool(ABC):
    """Base class for all tools."""
    name: str
    description: str
    parameters: Dict[str, Any]
    strict: bool = True

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool with the given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            str: Result of the tool execution as a string
        """
        raise NotImplementedError

    def to_openai_function(self) -> Dict[str, Any]:
        """Convert the tool to OpenAI function format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

def tool(name: Optional[str] = None, description: Optional[str] = None):
    """Decorator to register a tool class.
    
    Args:
        name: Optional name override for the tool
        description: Optional description override for the tool
    """
    def decorator(cls):
        if name is not None:
            cls.name = name
        if description is not None:
            cls.description = description
        return cls
    return decorator
