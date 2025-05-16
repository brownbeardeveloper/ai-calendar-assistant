"""
Main application class for the Calendar Assistant UI.
"""

from textual.app import App


class CalendarApp(App):
    """Main application class for the Calendar Assistant."""

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
        pass

    async def on_mount(self):
        """Handle the application mount event."""
        # Apply theme from settings if available
        if self.settings_controller:
            theme_result = self.settings_controller.get_theme()
            if theme_result["success"]:
                self.dark = theme_result["theme"] == "dark"
        pass

    async def on_load(self):
        """Handle the application load event."""
        pass

    def compose(self):
        """Compose the application layout."""
        pass

    async def action_toggle_dark(self):
        """Toggle dark mode."""
        self.dark = not self.dark
        # Update theme setting
        if self.settings_controller:
            theme = "dark" if self.dark else "light"
            self.settings_controller.set_theme(theme)
        pass

    async def action_quit(self):
        """Quit the application."""
        pass

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
