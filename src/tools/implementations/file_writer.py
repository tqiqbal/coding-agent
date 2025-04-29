"""File writer tool implementation."""
import os
from typing import List, Dict
from ..base import Tool, tool

@tool(
    name="write_files",
    description="Write content to one or more files"
)
class FileWriterTool(Tool):
    parameters = {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "description": "List of files to write",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path where the file should be written"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        },
                        "mode": {
                            "type": "string",
                            "description": "Write mode: 'w' for overwrite, 'a' for append",
                            "enum": ["w", "a"],
                            "default": "w"
                        }
                    },
                    "required": ["path", "content"],
                    "additionalProperties": False
                },
                "minItems": 1
            }
        },
        "required": ["files"],
        "additionalProperties": False
    }

    async def execute(self, files: List[Dict[str, str]]) -> str:
        """Write content to the specified files.
        
        Args:
            files: List of dictionaries containing:
                - path: Path where to write the file
                - content: Content to write
                - mode: Write mode ('w' for overwrite, 'a' for append)
            
        Returns:
            A string describing the results of the write operations
            
        Raises:
            ValueError: If any file cannot be written
        """
        results = []
        
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            mode = file_info.get("mode", "w")
            
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                
                # Write the file
                with open(path, mode, encoding='utf-8') as f:
                    f.write(content)
                
                action = "appended to" if mode == "a" else "written to"
                results.append(f"Successfully {action} {path}")
                
            except Exception as e:
                raise ValueError(f"Error writing to file {path}: {str(e)}")
        
        # Return summary
        return "\n".join(results)
