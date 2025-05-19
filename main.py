#!/usr/bin/env python3
"""
Entry point of the Calendar Assistant application.
"""

import traceback
import sys
import os
from dotenv import load_dotenv
from calendar_assistant.ui.app import CalendarApp
from calendar_assistant.controllers.app_controller import AppController


def main():
    """Main entry point of the application."""
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Print for debugging - can be removed once working
        print(
            f"Using OpenAI API key: {os.environ.get('OPENAI_API_KEY', 'Not set')[:5]}..."
        )

        controller = AppController()
        app = CalendarApp(controller=controller)
        app.run()

    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
