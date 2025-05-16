"""
Event list widget for the Calendar Assistant UI.
Uses Static widgets with panels for reliable display of calendar events.
"""

from textual.widgets import Static
from textual.containers import VerticalScroll
from rich.panel import Panel
from rich.text import Text
from datetime import datetime


class EventList(VerticalScroll):
    """Widget for displaying calendar events using direct Static widgets."""

    def __init__(self, title="Upcoming Events"):
        """Initialize the event list widget."""
        super().__init__()
        self.title = title
        self.events = []
        self.event_widgets = []
        print(f"EventList initialized with title: {title}")

    def compose(self):
        """Compose the widget layout."""
        print("EventList.compose() called")
        # Empty layout initially
        yield Static("Loading events...", id="loading-message")

    def on_mount(self):
        """Handle the widget mount event."""
        print(f"EventList.on_mount() called, setting title to: {self.title}")
        self.border_title = self.title

    def update_events(self, events):
        """Update the displayed events."""
        try:
            print(f"EventList.update_events() called with {len(events)} events")
            self.events = sorted(events, key=lambda e: e.get("start_time", ""))

            # Remove all existing widgets
            for widget in self.event_widgets:
                if widget.is_attached:
                    widget.remove()
            self.event_widgets = []

            # Try to remove loading message
            try:
                loading = self.query_one("#loading-message")
                if loading:
                    loading.remove()
                    print("Removed loading message")
            except Exception as e:
                print(f"Could not remove loading message: {e}")

            # If no events, show a message
            if not self.events:
                print("No events to display in EventList")
                no_events = Static("NO EVENTS SCHEDULED", classes="bold red")
                self.mount(no_events)
                self.event_widgets.append(no_events)
                return

            # Create a static widget for each event
            print(f"Adding {len(self.events)} events to EventList")
            for i, event in enumerate(self.events):
                try:
                    event_widget = self._create_event_widget(event, i)
                    self.mount(event_widget)
                    self.event_widgets.append(event_widget)
                    print(f"Added event widget {i + 1}: {event.get('title')}")
                except Exception as e:
                    print(f"Error adding event widget: {e}")
                    error_widget = Static(f"Error: {str(e)}", classes="error")
                    self.mount(error_widget)
                    self.event_widgets.append(error_widget)

            # Add a final spacer
            spacer = Static("", classes="spacer")
            self.mount(spacer)
            self.event_widgets.append(spacer)

        except Exception as e:
            print(f"Error updating events in EventList: {e}")
            import traceback

            traceback.print_exc()
            error_widget = Static(f"ERROR: {str(e)}", classes="error")
            self.mount(error_widget)
            self.event_widgets.append(error_widget)

    def _create_event_widget(self, event, index):
        """Create a static widget for an event."""
        title = event.get("title", "Untitled Event")
        start_time = self._format_time(event.get("start_time", ""))
        end_time = self._format_time(event.get("end_time", ""))
        description = event.get("description", "")

        # Format the event text
        event_text = Text()
        event_text.append(f"{start_time} - {end_time}", style="bold blue")
        event_text.append(f"\n{title}", style="bold")
        if description:
            event_text.append(f"\n{description}", style="italic")

        # Create a panel for better visibility
        panel = Panel(event_text, border_style="blue")

        # Create widget with unique ID
        widget_id = f"event-{event.get('id', index)}"
        return Static(panel, id=widget_id, classes="event-item")

    def _format_time(self, time_str):
        """Format a time string for display."""
        try:
            dt = datetime.fromisoformat(time_str)
            return dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            print(f"Error formatting time: {time_str}")
            return time_str or ""
