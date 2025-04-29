"""Entry point for the AI assistant."""
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.cli import app

if __name__ == "__main__":
    app()
