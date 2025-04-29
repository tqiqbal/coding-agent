"""Tool implementations package."""
from .time import CurrentTimeTool
from .file_reader import FileReaderTool
from .file_writer import FileWriterTool
from .string_replacer import StringReplacerTool

# List of all available tools
available_tools = [
    CurrentTimeTool,
    FileReaderTool,
    FileWriterTool,
    StringReplacerTool
]

__all__ = ['available_tools', 'CurrentTimeTool', 'FileReaderTool', 'FileWriterTool', 'StringReplacerTool']
