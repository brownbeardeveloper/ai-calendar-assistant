"""
Chat message widget for the Calendar Assistant UI.
"""

from datetime import datetime
from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text


class MessageWidget(Static):
    """Widget for displaying a chat message."""

    def __init__(self, sender, content, timestamp=None, is_user=False):
        """Initialize the message widget."""
        super().__init__()
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()
        self.is_user = is_user
        self.add_class("user" if is_user else "assistant")

    def render(self):
        """Render the message widget."""
        # Format the message content
        sender_text = Text(f"{self.sender}: ", style="bold")
        content_text = Text(self.content)
        time_text = Text(f"\n{self.format_timestamp()}", style="italic dim")

        combined_text = Text.assemble(sender_text, content_text, time_text)

        # Create a panel with the message content
        panel = Panel(
            combined_text,
            border_style="green" if self.is_user else "blue",
            title=self.sender,
            title_align="left",
            padding=(0, 1),
            highlight=True,
        )

        return panel

    def format_timestamp(self):
        """Format the message timestamp for display."""
        try:
            dt = datetime.fromisoformat(self.timestamp)
            return dt.strftime("%H:%M:%S")
        except (ValueError, TypeError):
            return self.timestamp or ""
