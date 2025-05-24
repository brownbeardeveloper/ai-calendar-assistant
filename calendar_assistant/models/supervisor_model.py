from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain_core.messages import SystemMessage

from calendar_assistant.models.google_calendar_model import GoogleCalendarModel
from calendar_assistant.prompts.agent_prompts import get_prompt


class SupervisorModel:
    """
    Handles the initialization and management of the AI agent for Google Calendar operations.
    """

    def __init__(
        self,
        google_calendar_model: GoogleCalendarModel,
        model_name: str = "gpt-4.1-nano",
    ):
        self.google_calendar_model = google_calendar_model
        self.model_name = model_name
        self.model = None
        self.agent_executor = None
        self.initialize()

    def _get_tools(self):
        """Define and return Google Calendar tool functions."""
        gcal_model = self.google_calendar_model

        @tool
        async def create_google_calendar_event(
            title: str,
            start_time: str,
            end_time: str = "",
            description: str = "",
            location: str = "",
            attendees: str = "",
        ) -> str:
            """
            Create a new event directly in Google Calendar.

            Args:
                title: The title of the event (required).
                start_time: The start time in ISO format YYYY-MM-DDTHH:MM:SS (required).
                            If no timezone is specified, UTC will be assumed by Google Calendar.
                end_time: The end time in ISO format YYYY-MM-DDTHH:MM:SS (optional).
                          Defaults to 1 hour after start_time. Assumes UTC if no timezone.
                description: Description of the event (optional).
                location: Where the event takes place (optional).
                attendees: Comma-separated email addresses of attendees (optional).
            """
            if not gcal_model.service:
                return "Error: Google Calendar service is not available. Please check authentication."
            try:
                # Prepare event data for GoogleCalendarModel.create_event
                event_data = {
                    "title": title,
                    "start_time": start_time,
                    "description": description,
                    "location": location,
                    "attendees": attendees,
                }
                if end_time:
                    event_data["end_time"] = end_time
                else:
                    start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                    event_data["end_time"] = (start_dt + timedelta(hours=1)).isoformat()

                created_event = gcal_model.create_event(event_data=event_data)

                if created_event and created_event.get("id"):
                    # Format confirmation message
                    start_dt_confirm = datetime.fromisoformat(
                        created_event["start_time"].replace("Z", "+00:00")
                    )
                    end_dt_confirm = datetime.fromisoformat(
                        created_event["end_time"].replace("Z", "+00:00")
                    )
                    loc_confirm = (
                        f" at {created_event['location']}"
                        if created_event.get("location")
                        else ""
                    )
                    return f"Successfully created Google Calendar event: '{created_event['title']}' from {start_dt_confirm.strftime('%Y-%m-%d %H:%M %Z')} to {end_dt_confirm.strftime('%H:%M %Z')}{loc_confirm}."
                else:
                    return "Error: Failed to create Google Calendar event. No event data returned."

            except ValueError as e:
                return f"Error creating event due to invalid date/time format: {str(e)}. Please use ISO YYYY-MM-DDTHH:MM:SS."
            except Exception as e:
                return f"Unexpected error creating Google Calendar event: {str(e)}"

        @tool
        async def get_google_calendar_today_events() -> str:
            """Get all events scheduled for today from Google Calendar."""
            if not gcal_model.service:
                return "Error: Google Calendar service is not available."
            try:
                today = datetime.now().date()
                start_date_dt = datetime.combine(today, datetime.min.time())
                end_date_dt = datetime.combine(
                    today + timedelta(days=1), datetime.min.time()
                )

                events = gcal_model.get_events(
                    start_date=start_date_dt.isoformat() + "Z",
                    end_date=end_date_dt.isoformat() + "Z",
                )
                if not events:
                    return "No events scheduled for today in Google Calendar."

                result = "Today's Google Calendar events:\n"
                for event in events:
                    title = event.get("title", "Untitled Google Event")
                    start_str = event.get("start_time", "")
                    loc = event.get("location", "")

                    try:
                        start_dt = datetime.fromisoformat(
                            start_str.replace("Z", "+00:00")
                        )
                        formatted_time = start_dt.strftime("%H:%M %Z")
                    except ValueError:
                        formatted_time = start_str

                    loc_info = f" at {loc}" if loc else ""
                    result += f"- {title} at {formatted_time}{loc_info}\n"

                return result.strip()
            except Exception as e:
                return f"Error retrieving today's Google Calendar events: {str(e)}"

        @tool
        async def get_google_calendar_events_for_date_range(
            start_date: str, end_date: str
        ) -> str:
            """
            Get events from Google Calendar within a specific date range.

            Args:
                start_date: The start date in ISO format YYYY-MM-DD (e.g., "2024-06-01"). Time is assumed as start of day.
                end_date: The end date in ISO format YYYY-MM-DD (e.g., "2024-06-07"). Time is assumed as end of day.
            """
            if not gcal_model.service:
                return "Error: Google Calendar service is not available."
            try:
                # Convert YYYY-MM-DD to YYYY-MM-DDTHH:MM:SSZ for full day coverage
                start_dt_iso = (
                    datetime.fromisoformat(start_date + "T00:00:00").isoformat() + "Z"
                )
                end_dt_iso = (
                    datetime.fromisoformat(end_date + "T23:59:59").isoformat() + "Z"
                )

                events = gcal_model.get_events(
                    start_date=start_dt_iso, end_date=end_dt_iso
                )
                if not events:
                    return f"No events found in Google Calendar between {start_date} and {end_date}."

                result = (
                    f"Google Calendar events between {start_date} and {end_date}:\n"
                )
                for event in events:
                    title = event.get("title", "Untitled Google Event")
                    start_str = event.get("start_time", "")
                    loc = event.get("location", "")
                    try:
                        start_dt = datetime.fromisoformat(
                            start_str.replace("Z", "+00:00")
                        )
                        formatted_time = start_dt.strftime("%Y-%m-%d %H:%M %Z")
                    except ValueError:
                        formatted_time = start_str
                    loc_info = f" at {loc}" if loc else ""
                    result += f"- {title} on {formatted_time}{loc_info}\n"
                return result.strip()
            except ValueError:
                return "Error: Invalid date format. Please use YYYY-MM-DD."
            except Exception as e:
                return (
                    f"Error retrieving Google Calendar events for date range: {str(e)}"
                )

        return [
            create_google_calendar_event,
            get_google_calendar_today_events,
            get_google_calendar_events_for_date_range,
        ]

    def initialize(self):
        """Initialize the LLM model and agent executor."""
        try:
            self.model = ChatOpenAI(model=self.model_name, temperature=0)
        except Exception as e:
            print(f"Error initializing ChatOpenAI: {e}")
            self.model = None
            return

        if not self.model:
            print("ChatOpenAI model could not be initialized. Agent setup aborted.")
            return

        tools = self._get_tools()
        system_message_content = get_prompt("supervisor_google_calendar")
        if not system_message_content:
            print("Error: Supervisor prompt could not be loaded. Agent setup aborted.")
            self.agent_executor = None
            return

        system_message = SystemMessage(content=system_message_content)

        try:
            agent = OpenAIFunctionsAgent.from_llm_and_tools(
                llm=self.model, tools=tools, system_message=system_message
            )
            self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        except Exception as e:
            print(f"Error creating agent executor: {e}")
            self.agent_executor = None

    async def process_message(self, user_input: str) -> str:
        """
        Process a user message through the agent.
        """
        if not self.agent_executor:
            return "Error: Agent not initialized. Cannot process message."
        try:
            # Add current date and time context to the user input
            now = datetime.now()
            current_date_str = now.strftime("%A, %B %d, %Y")
            current_time_str = now.strftime("%I:%M %p")
            current_timezone = now.astimezone().tzname()

            contextual_input = f"""
                                Current date and time context:
                                - Today is: {current_date_str}
                                - Current time: {current_time_str} {current_timezone}
                                - Current datetime (ISO): {now.isoformat()}

                                User request: {user_input}

                                Please interpret any relative date/time references (like "today", "yesterday", "tomorrow", "next week", etc.) based on the current date provided above.
                                """

            result = await self.agent_executor.ainvoke({"input": contextual_input})
            return result.get("output", "No output from agent.")
        except Exception as e:
            print(f"Error during agent processing: {e}")
            return f"I encountered an issue processing your request: {str(e)}"
