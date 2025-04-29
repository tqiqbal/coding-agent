"""Command-line interface for the AI assistant."""
import asyncio
import typer
from rich.prompt import Prompt
from src import config
from src.assistant import Assistant

app = typer.Typer()
assistant = Assistant()

@app.command()
def main():
    """Start the AI assistant CLI."""
    typer.echo("Welcome to the Terminal AI Assistant! Type 'exit' to quit or 'clear' to clear history.\n")
    
    async def chat_loop():
        while True:
            # Get user input
            user_input = Prompt.ask(f"{config.USER_PREFIX}")
            
            # Check for commands
            if user_input.lower() == 'exit':
                typer.echo("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                assistant.clear_history()
                typer.echo("Conversation history cleared.")
                continue
            
            # Get AI response
            await assistant.get_response(user_input)

    # Run the chat loop
    asyncio.run(chat_loop())

if __name__ == "__main__":
    app()
