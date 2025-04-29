"""File reader tool implementation."""
import os
from typing import List
from ..base import Tool, tool

@tool(
    name="read_files",
    description="Read the contents of one or more files"
)
class FileReaderTool(Tool):
    parameters = {
        "type": "object",
        "properties": {
            "file_paths": {
                "type": "array",
                "description": "List of file paths to read",
                "items": {
                    "type": "string",
                    "description": "Path to a file"
                },
                "minItems": 1
            }
        },
        "required": ["file_paths"],
        "additionalProperties": False
    }

    async def execute(self, file_paths: List[str]) -> str:
        """Read the contents of the specified files.
        
        Args:
            file_paths: List of paths to files to read
            
        Returns:
            A string containing the contents of all files, with headers
            
        Raises:
            ValueError: If any file cannot be read or does not exist
        """
        results = []
        
        for file_path in file_paths:
            try:
                # Verify the file exists and is a file (not a directory)
                if not os.path.isfile(file_path):
                    raise ValueError(f"Path does not exist or is not a file: {file_path}")
                
                # Check if the file is readable
                if not os.access(file_path, os.R_OK):
                    raise ValueError(f"File is not readable: {file_path}")
                
                # Read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add a header for this file's content
                results.append(f"\n=== File: {file_path} ===\n{content}")
                
            except Exception as e:
                raise ValueError(f"Error reading file {file_path}: {str(e)}")
        
        # Join all results with newlines
        return "\n".join(results)
