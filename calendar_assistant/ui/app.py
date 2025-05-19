# app.py

import traceback
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input
from textual.binding import Binding
from datetime import datetime
from typing import List, Dict, Any

from calendar_assistant.ui.widgets.message import MessageWidget
from calendar_assistant.ui.widgets.event_list import EventList
from calendar_assistant.ui.widgets.calendar_display import CalendarDisplay
from calendar_assistant.ui.widgets.css import CSS


class CalendarApp(App):
    """Main application class for the Calendar Assistant UI."""

    CSS = CSS
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.events = []

    async def on_mount(self):
        """Initialize UI and apply theme."""
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
            current_time = datetime.now()
            all_month_events = await self.controller.get_events_for_month(current_time)
            self.events = all_month_events  # For CalendarDisplay

            # Filter for today's and future events for the EventList
            today_date = current_time.date()
            upcoming_events = [
                event
                for event in all_month_events
                if datetime.fromisoformat(event["start_time"]).date() >= today_date
            ]

            self._update_ui_with_events(upcoming_events_for_list=upcoming_events)

            # Initialize chat area
            chat_container = self.query_one("#chat-container")
            chat_container.scroll_end(animate=False)

        except Exception as e:
            print(f"Error loading calendar events: {e}")
            traceback.print_exc()
            self.events = []

    def _update_ui_with_events(self, upcoming_events_for_list: List[Dict[str, Any]]):
        try:
            calendar_display = self.query_one(CalendarDisplay)
            if calendar_display:
                calendar_display.highlight_events(self.events)

            event_list = self.query_one(EventList)
            if event_list:
                event_list.border_title = "Today & Upcoming Events"
                event_list.update_events(upcoming_events_for_list)

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

    async def action_quit(self):
        self.exit()

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
