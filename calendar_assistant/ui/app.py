# calendar_ui.py

import asyncio
import traceback
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input
from textual.binding import Binding

from calendar_assistant.ui.widgets.message import MessageWidget
from calendar_assistant.ui.widgets.event_list import EventList
from calendar_assistant.ui.widgets.calendar_display import CalendarDisplay
from calendar_assistant.ui.widgets.css import CSS


class CalendarApp(App):
    """Main application class for the Calendar Assistant UI."""

    CSS = CSS

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("q", "quit", "Quit"),
        Binding("1", "chat_tab", "Chat Tab"),
        Binding("2", "calendar_tab", "Calendar Tab"),
    ]

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.events = []

    async def on_mount(self):
        """Initialize UI and apply theme."""
        self.dark = self.controller.get_theme() == "dark"
        try:
            self.query_one("#chat-input").focus()
        except Exception as e:
            print(f"Error focusing input: {e}")

    async def on_ready(self):
        """App is ready — load data."""
        await self.load_events()

    async def load_events(self):
        """Load upcoming events and update UI."""
        try:
            result = self.controller.get_upcoming_events(limit=None)
            if result["success"]:
                self.events = result["events"]
            else:
                self.events = []

            self._update_ui_with_events()
            # Initialize chat area
            chat_container = self.query_one("#chat-container")
            chat_container.scroll_end(animate=False)

        except Exception as e:
            print(f"Error loading calendar events: {e}")
            traceback.print_exc()
            self.events = []

    def _update_ui_with_events(self):
        try:
            calendar_display = self.query_one(CalendarDisplay)
            if calendar_display:
                calendar_display.highlight_events(self.events)

            event_list = self.query_one(EventList)
            if event_list:
                event_list.border_title = "Upcoming Events"
                event_list.update_events(self.events)

        except Exception as e:
            print(f"Error updating UI with events: {e}")
            traceback.print_exc()

    def compose(self):
        """Define the layout."""
        yield Header()
        with Horizontal():
            with Vertical(id="chat-section", classes="column"):
                with Vertical(id="chat-container", classes="chat-container"):
                    pass
                yield Input(placeholder="Type your message here...", id="chat-input")

            with Vertical(id="calendar-section", classes="column"):
                yield CalendarDisplay(events=self.events)
                yield EventList(title="Upcoming Events")
        yield Footer()

    async def action_toggle_dark(self):
        new_theme = self.controller.toggle_theme()
        self.dark = new_theme == "dark"

    async def action_quit(self):
        self.exit()

    async def action_chat_tab(self):
        self.query_one("#chat-input").focus()

    async def action_calendar_tab(self):
        self.query_one("#calendar-section").focus()

    async def on_input_submitted(self, event):
        """Handle chat input."""
        user_input = event.value.strip()
        if not user_input:
            return

        event.input.value = ""  # clear input

        chat_container = self.query_one("#chat-container")
        user_msg = MessageWidget("User", user_input, is_user=True)
        chat_container.mount(user_msg)
        chat_container.scroll_end(animate=False)

        try:
            assistant_text = await self.controller.process_chat(user_input)
        except Exception as e:
            assistant_text = f"Error: {e}"
            traceback.print_exc()

        assistant_msg = MessageWidget("Assistant", assistant_text)
        chat_container.mount(assistant_msg)
        chat_container.scroll_end(animate=False)

        self.query_one("#chat-input").focus()
