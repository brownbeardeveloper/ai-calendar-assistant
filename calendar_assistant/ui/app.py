"""
Main application class for the Calendar Assistant UI.
"""

import asyncio
import traceback
import json
import os
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static
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
        Binding("1", "chat_tab", "Chat Tab"),
        Binding("2", "calendar_tab", "Calendar Tab"),
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
        self.events = []

    async def on_mount(self):
        """Handle the application mount event."""
        # Apply theme from settings if available
        if self.settings_controller:
            theme_result = self.settings_controller.get_theme()
            if theme_result["success"]:
                self.dark = theme_result["theme"] == "dark"

        # Set up input handler
        try:
            input_widget = self.query_one("#chat-input")
            input_widget.focus()
        except Exception as e:
            print(f"Error setting up input handler: {e}")

    async def on_ready(self):
        """Called once when the app is ready."""
        # Load events and update the UI
        await self.load_events()

    async def load_events(self):
        """Load events from JSON file and update the UI."""
        try:
            # Load events from the real JSON file
            json_file_path = "data/calendar_data.json"
            if os.path.exists(json_file_path):
                try:
                    with open(json_file_path, "r") as f:
                        calendar_data = json.load(f)
                        # Store all events
                        self.all_events = sorted(
                            calendar_data, key=lambda e: e.get("start_time", "")
                        )
                        print(
                            f"Loaded {len(self.all_events)} events from JSON file: {json_file_path}"
                        )

                        # For the UI, only load upcoming events if calendar controller exists
                        if self.calendar_controller:
                            result = self.calendar_controller.get_upcoming_events(
                                limit=None
                            )
                            if result["success"]:
                                self.events = result["events"]
                                print(f"Filtered to {len(self.events)} upcoming events")
                            else:
                                self.events = self.all_events
                                print(
                                    "Failed to filter upcoming events, using all events"
                                )
                        else:
                            self.events = self.all_events
                            print("No calendar controller, using all events")
                except json.JSONDecodeError as je:
                    print(f"JSON decode error: {je}")
                    raise
                except Exception as e:
                    print(f"Error loading JSON data: {e}")
                    raise
            else:
                print(f"Calendar data file not found: {json_file_path}")
                raise FileNotFoundError(
                    f"Calendar data file not found: {json_file_path}"
                )

            # Update UI with loaded events
            self._update_ui_with_events()

            # Add sample messages for testing
            self._add_sample_chat_messages()

        except Exception as e:
            print(f"Error loading calendar data: {e}")
            traceback.print_exc()

            # Create empty array if no events could be loaded
            self.events = []
            print("No events loaded. UI will show empty state.")

    def _update_ui_with_events(self):
        """Update the UI components with loaded events."""
        try:
            # Update calendar display
            calendar_display = self.query_one(CalendarDisplay)
            if calendar_display:
                calendar_display.highlight_events(self.events)
                print(f"Highlighted {len(self.events)} events on calendar")

            # Update the events list
            event_list = self.query_one(EventList)
            if event_list:
                event_list.border_title = "Upcoming Events"

                # Update the events list
                try:
                    event_list.update_events(self.events)
                    print(f"Updated event list with {len(self.events)} events")
                except Exception as e:
                    print(f"Error updating event list: {e}")
                    traceback.print_exc()

                # Print actual events for debugging
                for i, event in enumerate(self.events):
                    print(
                        f"Event {i + 1}: {event.get('title')} - {event.get('start_time')}"
                    )
        except Exception as e:
            print(f"Error updating UI with events: {e}")
            traceback.print_exc()

    def _add_sample_chat_messages(self):
        """Add sample chat messages for testing."""
        try:
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
            print(f"Error adding sample messages: {e}")

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

                # Input area at bottom (only one input field)
                yield Input(placeholder="Type your message here...", id="chat-input")

            # Calendar section (1/2 of width)
            with Vertical(id="calendar-section", classes="column"):
                # Calendar display
                yield CalendarDisplay(events=self.events)

                # Using the event list
                yield EventList(title="Upcoming Events")

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

    async def action_chat_tab(self):
        """Focus chat tab."""
        self.query_one("#chat-input").focus()

    async def action_calendar_tab(self):
        """Focus calendar tab."""
        self.query_one("#calendar-section").focus()

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
