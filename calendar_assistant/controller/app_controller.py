from calendar_assistant.models.calendar_model import CalendarModel
from calendar_assistant.models.chat_model import ChatModel
from calendar_assistant.models.settings_model import SettingsModel


class AppController:
    def __init__(self):
        self.calendar = CalendarModel()
        self.chat = ChatModel()
        self.settings = SettingsModel()

    # Chat
    async def process_chat(self, user_input: str) -> str:
        """Process a user query through the agent and log the conversation."""
        if not user_input.strip():
            return "Empty input received."

        self.chat.add(user_input)
        response = self.chat.process(user_input)
        self.chat.add(response)
        return response

    # Calendar
    def get_upcoming_events(self, limit=5):
        return self.calendar.get_upcoming_events(limit)

    def get_today_events(self):
        return self.calendar.get_today_events()

    def create_event(self, title, start_time, end_time, description=None):
        return self.calendar.create_event(title, start_time, end_time, description)

    def update_event(
        self, event_id, title=None, start_time=None, end_time=None, description=None
    ):
        return self.calendar.update_event(
            event_id, title, start_time, end_time, description
        )

    def delete_event(self, event_id):
        return self.calendar.delete_event(event_id)

    # Settings
    def get_settings(self):
        return self.settings.get_settings()

    def toggle_theme(self):
        current = self.settings.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        self.settings.set("theme", new_theme)
        return new_theme

    def get_theme(self):
        return self.settings.get("theme", "dark")
