#!/usr/bin/env python3
"""
Entry point of the Calendar Assistant application.
"""

from calendar_assistant.ui.app import CalendarApp
from calendar_assistant.core.supervisor_controller import SupervisorController
from calendar_assistant.controllers.calendar_controller import CalendarController
from calendar_assistant.controllers.chat_controller import ChatController
from calendar_assistant.controllers.settings_controller import SettingsController


def main():
    """Main entry point of the application."""
    # Initialize controllers
    calendar_controller = CalendarController()
    chat_controller = ChatController()
    settings_controller = SettingsController()

    # Initialize the supervisor controller with our domain controllers
    supervisor = SupervisorController()
    supervisor.initialize_agents()

    # Initialize and run the UI app with the controllers
    app = CalendarApp(
        supervisor=supervisor,
        calendar_controller=calendar_controller,
        chat_controller=chat_controller,
        settings_controller=settings_controller,
    )
    app.run()


if __name__ == "__main__":
    main()
