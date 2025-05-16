"""
Event list widget for the Calendar Assistant UI.
"""

from datetime import datetime
from textual.widgets import ListView, ListItem
from textual.containers import VerticalScroll
from rich.text import Text


class EventList(VerticalScroll):
    """Widget for displaying a list of calendar events."""

    def __init__(self, title="Today's Events"):
        """Initialize the event list widget."""
        super().__init__()
        self.title = title
        self.events = []
        self.event_list = ListView()

    def compose(self):
        """Compose the widget layout."""
        self.event_list = ListView()
        yield self.event_list

    def on_mount(self):
        """Handle the widget mount event."""
        self.border_title = self.title

    def update_events(self, events):
        """Update the displayed events."""
        self.events = sorted(events, key=lambda e: e.get("start_time", ""))
        self.event_list.clear()

        # If no events, show a message
        if not self.events:
            self.event_list.append(
                ListItem(Text("No events scheduled", style="italic"))
            )
            return

        # Add events to the list
        for event in self.events:
            self.event_list.append(self._create_event_item(event))

    def _create_event_item(self, event):
        """Create a list item for an event."""
        title = event.get("title", "Untitled Event")
        start_time = self._format_time(event.get("start_time", ""))
        end_time = self._format_time(event.get("end_time", ""))
        description = event.get("description", "")

        # Format the event item
        event_text = Text()
        event_text.append(f"{start_time} - {end_time}", style="bold blue")
        event_text.append(f"\n{title}", style="bold")
        if description:
            event_text.append(f"\n{description}", style="italic")

        return ListItem(event_text, id=event.get("id"))

    def _format_time(self, time_str):
        """Format a time string for display."""
        try:
            dt = datetime.fromisoformat(time_str)
            return dt.strftime("%H:%M")
        except (ValueError, TypeError):
            return time_str or ""

    def on_list_view_selected(self, event):
        """Handle event selection."""
        selected_item = event.item
        if selected_item and hasattr(selected_item, "id"):
            self.emit_no_wait("event_selected", event_id=selected_item.id)

    def on_event_click(self, event_id):
        """Handle click on an event."""
        pass

    def filter_events(self, filter_func):
        """Filter the displayed events."""
        pass
