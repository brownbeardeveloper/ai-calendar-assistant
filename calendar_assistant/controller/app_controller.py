from datetime import datetime
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from calendar_assistant.models.calendar_model import CalendarModel
from calendar_assistant.models.supervisor_model import SupervisorModel


class AppController:
    def __init__(self):
        self.calendar = CalendarModel()
        self.supervisor = None
        self._init_model()

    def _init_model(self):
        """Initialize the supervisor model if OpenAI API key is available."""
        load_dotenv()  # Load .env file if exists
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["OPENAI_MODEL"] = model_name

            # Initialize the supervisor model
            self.supervisor = SupervisorModel(
                calendar_model=self.calendar, model_name=model_name
            )

    # Calendar functions
    async def get_events_for_month(self, date: datetime) -> List[Dict[str, Any]]:
        return await self.calendar.get_events_for_month(date)

    async def get_today_events(self) -> List[Dict[str, Any]]:
        return await self.calendar.get_today_events()

    async def process_chat(self, user_input: str) -> str:
        """Processes user input from the chat interface using LLM."""
        # If model isn't initialized, return simple echo response
        if not self.supervisor:
            return f"Model not initialized (missing API key). Echo: {user_input}"

        try:
            # Process the message through the supervisor
            return await self.supervisor.process_message(user_input)

        except Exception as e:
            # Provide a simple fallback if processing fails
            print(f"Processing error: {e}")
            return (
                f"I couldn't process that request properly. Technical detail: {str(e)}"
            )
