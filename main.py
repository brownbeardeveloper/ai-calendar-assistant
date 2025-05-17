#!/usr/bin/env python3
"""
Entry point of the Calendar Assistant application.
"""

import traceback
import sys
from calendar_assistant.ui.app import CalendarApp
from calendar_assistant.controllers.calendar_controller import CalendarController
from calendar_assistant.core.supervisor_controller import SupervisorController


def main():
    """Main entry point of the application."""
    try:
        # Initialize controllers
        calendar_controller = CalendarController()
        supervisor_controller = SupervisorController()

        # Initialize and run the UI app with controllers
        app = CalendarApp(
            calendar_controller=calendar_controller, supervisor=supervisor_controller
        )
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
