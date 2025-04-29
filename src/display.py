"""Terminal display handling for the AI assistant."""
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text
from rich import box
from rich.panel import Panel
from src import config

console = Console()

class Display:
    def __init__(self):
        self.console = console
        self._current_response = ""
        self._live = None

    def show_user_input(self, text: str) -> None:
        """Display user input with appropriate styling."""
        self.console.print(f"\n{config.USER_PREFIX}", style=config.USER_COLOR, end="")
        self.console.print(text)

    def start_streaming(self) -> None:
        """Initialize streaming display."""
        self._current_response = ""
        self._live = Live(
            Panel("", title=config.PROMPT_PREFIX, box=box.ROUNDED),
            console=self.console,
            refresh_per_second=10
        )
        self._live.start()

    def update_streaming(self, new_text: str) -> None:
        """Update the streaming display with new text."""
        self._current_response += new_text
        if self._live:
            # Convert markdown in the response
            md = Markdown(self._current_response)
            self._live.update(Panel(md, title=config.PROMPT_PREFIX, box=box.ROUNDED))

    def end_streaming(self) -> None:
        """End the streaming display."""
        if self._live:
            self._live.stop()
            self._live = None

    def show_error(self, error: str) -> None:
        """Display an error message."""
        self.console.print(f"\n{config.ERROR_PREFIX}{error}", style=config.ERROR_COLOR)

    def show_thinking(self) -> None:
        """Display thinking indicator."""
        self._live = Live(
            Text(config.THINKING_TEXT, style=config.SYSTEM_COLOR),
            console=self.console,
            refresh_per_second=4
        )
        self._live.start()

    def clear_thinking(self) -> None:
        """Clear the thinking indicator."""
        if self._live:
            self._live.stop()
