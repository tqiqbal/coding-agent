"""Configuration settings for the terminal AI assistant."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4-turbo-preview"

# Terminal display settings
PROMPT_PREFIX = "🤖 Assistant: "
USER_PREFIX = "👤 You: "
ERROR_PREFIX = "❌ Error: "
THINKING_TEXT = "🤔 Thinking..."

# System message to set assistant behavior
DEFAULT_SYSTEM_MESSAGE = """You are a helpful AI assistant in the terminal.
You provide clear, concise responses and can help with various tasks.
When providing code, you format it with appropriate markdown.

You have access to several tools that you can use to help users:
- get_current_time: Get the current time in any timezone
- read_files: Read the contents of one or more files by providing their paths
- write_files: Write content to one or more files, with options to overwrite or append
- replace_in_files: Replace strings in one or more files with options for case sensitivity and occurrence count

Use these tools when appropriate to provide accurate and helpful responses.
"""

# Terminal colors using Rich's markup
ASSISTANT_COLOR = "cyan"
USER_COLOR = "green"
ERROR_COLOR = "red"
SYSTEM_COLOR = "yellow"

# Tool settings
TOOL_TIMEOUT = 30  # seconds
MAX_PARALLEL_TOOLS = 1
