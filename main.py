#!/usr/bin/env python3
"""
Entry point of the Calendar Assistant application.
"""

import traceback
import sys
import os
from calendar_assistant.ui.app import CalendarApp


def main():
    """Main entry point of the application."""
    try:
        # Initialize and run the UI app
        app = CalendarApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
