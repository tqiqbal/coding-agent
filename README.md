# Terminal AI Assistant

A command-line AI assistant using OpenAI's streaming API for real-time responses.

## Features

- Real-time streaming of AI responses
- Beautiful terminal formatting
- Command history
- System message support
- Error handling

## Setup

1. Clone the repository
2. Create a virtual environment (already done):
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key
   ```

## Usage

Run the assistant:
```bash
python src/cli.py
```
