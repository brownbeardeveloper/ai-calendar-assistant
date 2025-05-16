"""
Main application class for the Calendar Assistant UI.
"""

import asyncio
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input
from textual.binding import Binding

from calendar_assistant.ui.widgets.message import MessageWidget
from calendar_assistant.ui.widgets.event_list import EventList
from calendar_assistant.ui.widgets.calendar_display import CalendarDisplay
from calendar_assistant.ui.widgets.css import CSS


class CalendarApp(App):
    """Main application class for the Calendar Assistant."""

    CSS = CSS

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        supervisor=None,
        calendar_controller=None,
        chat_controller=None,
        settings_controller=None,
    ):
        """Initialize the calendar application."""
        super().__init__()
        # Controllers
        self.supervisor = supervisor
        self.calendar_controller = calendar_controller
        self.chat_controller = chat_controller
        self.settings_controller = settings_controller
        # Sample data for testing
        self.sample_events = []

    async def on_mount(self):
        """Handle the application mount event."""
        # Apply theme from settings if available
        if self.settings_controller:
            theme_result = self.settings_controller.get_theme()
            if theme_result["success"]:
                self.dark = theme_result["theme"] == "dark"

        # Set up input handler
        input_widget = self.query_one("#chat-input")
        input_widget.focus()

    async def on_ready(self):
        """Called once when the app is ready."""
        # Load sample events for testing
        await self.load_sample_data()

    async def load_sample_data(self):
        """Load sample events and messages for testing."""
        try:
            # Try to get events from controller first
            if self.calendar_controller:
                result = self.calendar_controller.get_events_for_day()
                if result["success"]:
                    self.sample_events = result["events"]

            # If no events from controller, use hardcoded sample
            if not self.sample_events:
                import json
                import os

                if os.path.exists("data/calendar_data.json"):
                    with open("data/calendar_data.json", "r") as f:
                        self.sample_events = json.load(f)

            # Update calendar and event list with sample data
            calendar_display = self.query_one(CalendarDisplay)
            if calendar_display:
                calendar_display.highlight_events(self.sample_events)

            event_list = self.query_one(EventList)
            if event_list:
                event_list.update_events(self.sample_events)

            # Add sample messages for testing
            chat_container = self.query_one("#chat-container")
            if chat_container:
                chat_container.mount(
                    MessageWidget(
                        "User",
                        "Hello, can you help me manage my calendar?",
                        is_user=True,
                    )
                )
                chat_container.mount(
                    MessageWidget(
                        "Assistant",
                        "Yes, I can help you manage your calendar. What would you like to do?",
                    )
                )

                # Scroll to bottom
                chat_container.scroll_end(animate=False)

        except Exception as e:
            print(f"Error loading sample data: {e}")

    async def on_load(self):
        """Handle the application load event."""
        # No additional bindings needed as they're defined in BINDINGS class variable
        pass

    def compose(self):
        """Compose the application layout."""
        yield Header()

        # Main layout: chat on left, calendar on right
        with Horizontal():
            # Chat section (1/2 of width)
            with Vertical(id="chat-section", classes="column"):
                # Chat messages container
                with Vertical(id="chat-container", classes="chat-container"):
                    # Messages will be added here
                    pass

                # Input area at bottom
                yield Input(placeholder="Type your message here...", id="chat-input")

            # Calendar section (1/2 of width)
            with Vertical(id="calendar-section", classes="column"):
                # Calendar display
                yield CalendarDisplay(events=self.sample_events)

                # Today's events list
                yield EventList(title="Today's Events")

        yield Footer()

    async def action_toggle_dark(self):
        """Toggle dark mode."""
        self.dark = not self.dark
        # Update theme setting
        if self.settings_controller:
            theme = "dark" if self.dark else "light"
            self.settings_controller.set_theme(theme)

    async def action_quit(self):
        """Quit the application."""
        self.exit()

    async def on_input_submitted(self, event):
        """Handle input submission."""
        user_input = event.value
        if not user_input.strip():
            return

        # Clear input
        event.input.value = ""

        # Display user message
        chat_container = self.query_one("#chat-container")
        user_msg = MessageWidget("User", user_input, is_user=True)
        chat_container.mount(user_msg)

        # Scroll to show the message
        chat_container.scroll_end(animate=False)

        # Small delay to simulate processing
        await asyncio.sleep(0.5)

        # For testing, just echo the message without LLM
        assistant_msg = MessageWidget(
            "Assistant", f"GUI Test Mode - You said: {user_input}"
        )
        chat_container.mount(assistant_msg)

        # Scroll again to show the response
        chat_container.scroll_end(animate=False)

        # Refocus the input field
        self.query_one("#chat-input").focus()

    async def process_user_input(self, user_input):
        """Process user input through the supervisor controller."""
        if self.supervisor:
            return await self.supervisor.process_user_request(user_input)
        return "Supervisor controller not initialized."

    async def get_calendar_events(self, date=None):
        """Get calendar events for a specific date."""
        if self.calendar_controller:
            return self.calendar_controller.get_events_for_day(date)
        return {"success": False, "error": "Calendar controller not initialized."}

    async def get_chat_history(self, limit=None):
        """Get chat history, optionally limited."""
        if self.chat_controller:
            return self.chat_controller.get_conversation_history(limit)
        return {"success": False, "error": "Chat controller not initialized."}

    async def get_app_settings(self):
        """Get application settings."""
        if self.settings_controller:
            return self.settings_controller.get_all_settings()
        return {"success": False, "error": "Settings controller not initialized."}
