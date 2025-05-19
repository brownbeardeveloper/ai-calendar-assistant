# app.py

import traceback
import asyncio
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static
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

            today_date = current_time.date()
            upcoming_events = []
            for event in all_month_events:
                start_time_obj = event.get("start_time")
                if isinstance(start_time_obj, datetime):
                    if start_time_obj.date() >= today_date:
                        upcoming_events.append(event)

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
                event_list.update_events(upcoming_events_for_list)

        except Exception as e:
            print(f"Error updating UI with events: {e}")
            traceback.print_exc()

    def compose(self):
        """Define the layout."""
        yield Header()
        with Horizontal():
            with Vertical(id="chat-section", classes="column"):
                # Create chat container with vertical layout to ensure messages stack properly
                with Vertical(id="chat-container", classes="chat-container"):
                    # Start with an empty chat container that will be filled with messages
                    pass
                yield Input(placeholder="Type your message here...", id="chat-input")

            with Vertical(id="calendar-section", classes="column"):
                yield CalendarDisplay(events=self.events)
                yield EventList()
        yield Footer()

    async def action_quit(self):
        self.exit()

    def on_input_submitted(self, event):
        """Handle chat input synchronously to ensure immediate UI update."""
        user_input = event.value.strip()
        if not user_input:
            return

        # Clear input field immediately
        event.input.value = ""

        # Add user message to chat - this happens synchronously
        chat_container = self.query_one("#chat-container")
        user_msg = MessageWidget("User", user_input)
        chat_container.mount(user_msg)
        chat_container.scroll_end(animate=False)

        # Focus on input immediately
        self.query_one("#chat-input").focus()

        # Store the user input for async processing
        self._last_user_input = user_input

        # Schedule AI processing after this refresh cycle completes
        self.call_after_refresh(self._schedule_ai_processing)

    def _schedule_ai_processing(self):
        """Schedule AI processing as a separate task after UI refresh."""
        # Create a separate background task for AI processing
        asyncio.create_task(self._process_ai_response(self._last_user_input))

    async def _process_ai_response(self, user_input: str):
        """Process AI response in a separate task."""
        chat_container = self.query_one("#chat-container")

        try:
            # Get AI response (this might take some time)
            assistant_text = await self.controller.process_chat(user_input)

            # Add assistant message
            assistant_msg = MessageWidget("Assistant", assistant_text)
            chat_container.mount(assistant_msg)
            chat_container.scroll_end(animate=False)
        except Exception as e:
            traceback.print_exc()
            # Show error message in chat
            error_msg = MessageWidget(
                "Assistant", f"Sorry, I encountered an error: {str(e)}"
            )
            chat_container.mount(error_msg)
            chat_container.scroll_end(animate=False)
