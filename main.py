#!/usr/bin/env python3
"""
Entry point of the Calendar Assistant application.
"""

import traceback
from calendar_assistant.ui.app import CalendarApp


def main():
    """Main entry point of the application."""
    try:
        # Initialize and run just the UI app without controllers for testing
        app = CalendarApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
