"""String replacement tool implementation."""
import os
from typing import List, Dict
from ..base import Tool, tool

@tool(
    name="replace_in_files",
    description="Replace strings in one or more files"
)
class StringReplacerTool(Tool):
    parameters = {
        "type": "object",
        "properties": {
            "replacements": {
                "type": "array",
                "description": "List of replacement operations to perform",
                "items": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to modify"
                        },
                        "old_string": {
                            "type": "string",
                            "description": "String to be replaced"
                        },
                        "new_string": {
                            "type": "string",
                            "description": "String to replace with"
                        },
                        "case_sensitive": {
                            "type": "boolean",
                            "description": "Whether the replacement should be case sensitive",
                            "default": True
                        },
                        "all_occurrences": {
                            "type": "boolean",
                            "description": "Whether to replace all occurrences or just the first one",
                            "default": True
                        }
                    },
                    "required": ["file_path", "old_string", "new_string"],
                    "additionalProperties": False
                },
                "minItems": 1
            }
        },
        "required": ["replacements"],
        "additionalProperties": False
    }

    async def execute(self, replacements: List[Dict[str, any]]) -> str:
        """Replace strings in the specified files.
        
        Args:
            replacements: List of dictionaries containing:
                - file_path: Path to the file to modify
                - old_string: String to be replaced
                - new_string: String to replace with
                - case_sensitive: Whether the replacement should be case sensitive (default: True)
                - all_occurrences: Whether to replace all occurrences (default: True)
            
        Returns:
            A string describing the results of the replacement operations
            
        Raises:
            ValueError: If any file cannot be read/written or if strings not found
        """
        results = []
        
        for rep in replacements:
            path = rep["file_path"]
            old_str = rep["old_string"]
            new_str = rep["new_string"]
            case_sensitive = rep.get("case_sensitive", True)
            all_occurrences = rep.get("all_occurrences", True)
            
            try:
                # Verify the file exists and is readable
                if not os.path.isfile(path):
                    raise ValueError(f"File does not exist: {path}")
                if not os.access(path, os.R_OK | os.W_OK):
                    raise ValueError(f"File is not readable/writable: {path}")
                
                # Read the file content
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Prepare strings for replacement
                if not case_sensitive:
                    # For case-insensitive search, we need to use string methods
                    import re
                    pattern = re.compile(re.escape(old_str), re.IGNORECASE)
                    if all_occurrences:
                        new_content = pattern.sub(new_str, content)
                    else:
                        new_content = pattern.sub(new_str, content, count=1)
                else:
                    # For case-sensitive search, we can use string methods
                    if all_occurrences:
                        new_content = content.replace(old_str, new_str)
                    else:
                        new_content = content.replace(old_str, new_str, 1)
                
                # Only write if changes were made
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    count = new_content.count(new_str) - content.count(new_str)
                    results.append(f"Successfully replaced {count} occurrence(s) in {path}")
                else:
                    results.append(f"No replacements made in {path} - string not found")
                
            except Exception as e:
                raise ValueError(f"Error processing file {path}: {str(e)}")
        
        # Return summary
        return "\n".join(results)
