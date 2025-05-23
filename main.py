#!/usr/bin/env python3
"""
Entry point of the Calendar Assistant application.
"""

import sys
from dotenv import load_dotenv
from calendar_assistant.ui.app import CalendarApp
from calendar_assistant.controller.app_controller import AppController


def main():
    """Main entry point of the application."""
    try:
        load_dotenv()
        controller = AppController()
        app = CalendarApp(controller=controller)
        app.run()

    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
