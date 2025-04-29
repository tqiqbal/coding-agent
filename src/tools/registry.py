"""Tool registry and management system."""
from typing import Dict, List, Type, Any
import asyncio
from .base import Tool

class ToolRegistry:
    """Registry for managing and executing tools."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool_class: Type[Tool]) -> None:
        """Register a tool class.
        
        Args:
            tool_class: The tool class to register
        """
        tool_instance = tool_class()
        self._tools[tool_instance.name] = tool_instance

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all registered tools in OpenAI function format.
        
        Returns:
            List of tool definitions in OpenAI function format
        """
        return [tool.to_openai_function() for tool in self._tools.values()]

    async def execute_tool(self, name: str, **kwargs) -> str:
        """Execute a tool by name with given arguments.
        
        Args:
            name: Name of the tool to execute
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool execution result as a string
            
        Raises:
            KeyError: If tool not found
            Exception: If tool execution fails
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")

        try:
            # Add timeout to tool execution
            result = await asyncio.wait_for(
                self._tools[name].execute(**kwargs),
                timeout=30  # 30 second timeout
            )
            return str(result)
        except asyncio.TimeoutError:
            return f"Error: Tool '{name}' execution timed out"
        except Exception as e:
            return f"Error executing tool '{name}': {str(e)}"
