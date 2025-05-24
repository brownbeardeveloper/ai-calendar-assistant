from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from calendar_assistant.models.google_calendar_model import GoogleCalendarModel
from calendar_assistant.models.supervisor_model import SupervisorModel


class AppController:
    def __init__(self):
        self.google_calendar = GoogleCalendarModel()
        self.supervisor = None
        self._init_model()

    def _init_model(self):
        """Initialize the supervisor model if OpenAI API key is available."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["OPENAI_MODEL"] = model_name

            # Initialize the supervisor model, now passing google_calendar
            self.supervisor = SupervisorModel(
                google_calendar_model=self.google_calendar, model_name=model_name
            )
        else:
            print("⚠️ OpenAI API key not found. Supervisor model not initialized.")

    # Calendar functions now solely use Google sync
    async def get_events_for_month(self, date: datetime) -> List[Dict[str, Any]]:
        """Get events for a month from Google Calendar."""
        google_events = []
        if self.google_calendar.service:
            try:
                start_date_dt = date.replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                )
                if date.month == 12:
                    end_date_dt = start_date_dt.replace(year=date.year + 1, month=1)
                else:
                    end_date_dt = start_date_dt.replace(month=date.month + 1)

                google_events = self.google_calendar.get_events(
                    start_date=start_date_dt.isoformat() + "Z",
                    end_date=end_date_dt.isoformat() + "Z",
                    max_results=250,
                )
            except Exception as e:
                print(f"Error fetching Google Calendar events for month: {e}")

        return self._deduplicate_events(google_events)

    async def get_today_events(self) -> List[Dict[str, Any]]:
        """Get today's events from Google Calendar."""
        google_events = []
        if self.google_calendar.service:
            try:
                today = datetime.now().date()
                start_date_dt = datetime.combine(today, datetime.min.time())
                end_date_dt = datetime.combine(
                    today + timedelta(days=1), datetime.min.time()
                )

                google_events = self.google_calendar.get_events(
                    start_date=start_date_dt.isoformat() + "Z",
                    end_date=end_date_dt.isoformat() + "Z",
                    max_results=100,
                )
            except Exception as e:
                print(f"Error fetching today's Google Calendar events: {e}")

        return self._deduplicate_events(google_events)

    def _deduplicate_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate events based on title and start time."""
        seen = set()
        unique_events = []

        for event in events:
            title = event.get("title", "").lower().strip()
            start_time = event.get("start_time", "")
            normalized_start = self._normalize_datetime_string(start_time)

            key = (title, normalized_start)

            if key not in seen and title:
                seen.add(key)
                unique_events.append(event)

        def get_sort_key(event_item):
            event_start_time = event_item.get("start_time", "")
            if isinstance(event_start_time, str):
                try:
                    # Parse datetime and ensure it's timezone-aware for consistent comparison
                    dt = datetime.fromisoformat(event_start_time.replace("Z", "+00:00"))
                    # If it doesn't have timezone info, make it UTC
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
                    return dt
                except ValueError:
                    # If parsing fails, return a very early date for sorting
                    return datetime.min.replace(
                        tzinfo=datetime.now().astimezone().tzinfo
                    )
            elif hasattr(event_start_time, "isoformat"):
                # Ensure datetime object has timezone info
                if event_start_time.tzinfo is None:
                    event_start_time = event_start_time.replace(
                        tzinfo=datetime.now().astimezone().tzinfo
                    )
                return event_start_time
            else:
                # Fallback for unexpected types
                return datetime.min.replace(tzinfo=datetime.now().astimezone().tzinfo)

        unique_events.sort(key=get_sort_key)
        return unique_events

    def _normalize_datetime_string(self, datetime_input) -> str:
        """Normalize datetime strings or objects for better duplicate detection."""
        if not datetime_input:
            return ""

        dt_str = ""
        if isinstance(datetime_input, datetime):
            dt_str = datetime_input.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(datetime_input, str):
            dt_str = datetime_input
        else:
            dt_str = str(datetime_input)

        try:
            parsed_dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return parsed_dt.strftime("%Y-%m-%dT%H:%M:%S")

        except ValueError:
            if "T" not in dt_str and len(dt_str) == 10:
                return dt_str + "T00:00:00"
            return dt_str

    async def process_chat(self, user_input: str) -> str:
        """Processes user input from the chat interface using LLM."""
        if not self.supervisor:
            return f"Model not initialized (missing API key). Echo: {user_input}"

        try:
            response = await self.supervisor.process_message(user_input)

            return response

        except Exception as e:
            print(f"Processing error in AppController: {e}")
            return (
                f"I couldn't process that request properly. Technical detail: {str(e)}"
            )

    async def process_chat_with_history(
        self, user_input: str, conversation_history: list
    ) -> str:
        """Processes user input with conversation history for context."""
        if not self.supervisor:
            return f"Model not initialized (missing API key). Echo: {user_input}"

        try:
            # Create a contextual prompt that includes recent conversation
            context_prompt = self._build_context_prompt(
                conversation_history, user_input
            )
            response = await self.supervisor.process_message(context_prompt)

            return response

        except Exception as e:
            print(f"Processing error in AppController: {e}")
            return (
                f"I couldn't process that request properly. Technical detail: {str(e)}"
            )

    def _build_context_prompt(
        self, conversation_history: list, current_input: str
    ) -> str:
        """Build a contextual prompt that includes recent conversation history and current date context."""
        # Add current date and time context
        now = datetime.now()
        current_date_str = now.strftime("%A, %B %d, %Y")
        current_time_str = now.strftime("%I:%M %p")
        current_timezone = now.astimezone().tzname()

        context_lines = ["Current date and time context:"]
        context_lines.append(f"- Today is: {current_date_str}")
        context_lines.append(f"- Current time: {current_time_str} {current_timezone}")
        context_lines.append(f"- Current datetime (ISO): {now.isoformat()}")
        context_lines.append("")

        # Get the last few exchanges for context (excluding current input)
        recent_history = (
            conversation_history[-6:]
            if len(conversation_history) > 6
            else conversation_history[:-1]
        )

        if recent_history:
            context_lines.append("Recent conversation context:")
            for msg in recent_history:
                role = msg["role"].title()
                content = msg["content"]
                context_lines.append(f"{role}: {content}")
            context_lines.append("")

        context_lines.append(f"Current request: {current_input}")
        context_lines.append(
            '\nPlease interpret any relative date/time references (like "today", "yesterday", "tomorrow", "next week", etc.) based on the current date provided above. Respond to the current request, taking into account the conversation context.'
        )

        return "\n".join(context_lines)
