from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain_core.messages import SystemMessage

from calendar_assistant.models.calendar_model import CalendarModel
from calendar_assistant.prompts.agent_prompts import get_prompt


class SupervisorModel:
    """
    Handles the initialization and management of the AI agent for calendar operations.
    """

    def __init__(self, calendar_model: CalendarModel, model_name: str = "gpt-4.1-nano"):
        self.calendar_model = calendar_model
        self.model_name = model_name
        self.model = None
        self.agent_executor = None
        self.initialize()

    def _get_tools(self):
        """Define and return calendar tool functions with access to the calendar model."""
        calendar_model = self.calendar_model

        @tool
        async def create_event(
            title: str,
            start_time: str,
            end_time: str = "",
            description: str = "",
            location: str = "",
            attendees: str = "",
        ) -> str:
            """
            Create a new calendar event.

            Args:
                title: The title of the event (required)
                start_time: The start time in ISO format YYYY-MM-DDTHH:MM:SS (required)
                end_time: The end time in ISO format YYYY-MM-DDTHH:MM:SS (optional, defaults to 1 hour after start time)
                description: Description of the event (optional)
                location: Where the event takes place (optional)
                attendees: People attending the event, comma separated (optional)
            """
            try:
                # Parse start time
                start_datetime = datetime.fromisoformat(start_time)

                # If end_time not provided, set it to 1 hour after start time
                if not end_time:
                    end_datetime = start_datetime + timedelta(hours=1)
                else:
                    end_datetime = datetime.fromisoformat(end_time)

                # Only add attendees to description
                if attendees:
                    description += f"\nAttendees: {attendees}"

                # Create the event with location as a separate field
                event = calendar_model.create_event(
                    title=title,
                    start_time=start_datetime,
                    end_time=end_datetime,
                    description=description.strip(),
                    location=location,
                )

                # Return success message
                return f"Successfully created event: '{event.title}' from {event.start_time.strftime('%Y-%m-%d %H:%M')} to {event.end_time.strftime('%H:%M')}{' at ' + location if location else ''}"

            except ValueError as e:
                return f"Error creating event: {str(e)}"
            except Exception as e:
                return f"Unexpected error creating event: {str(e)}"

        @tool
        async def get_today_events() -> str:
            """
            Get all events scheduled for today.
            """
            try:
                events = await calendar_model.get_today_events()
                if not events:
                    return "No events scheduled for today."

                result = "Today's events:\n"
                for event in events:
                    if isinstance(event, dict):
                        title = event.get("title", "Untitled")
                        start = event.get("start_time")
                        location = event.get("location", "")

                        if isinstance(start, str):
                            start_time = datetime.fromisoformat(start)
                            formatted_time = start_time.strftime("%H:%M")
                        else:
                            formatted_time = "Unknown time"

                        location_info = f" at {location}" if location else ""
                        result += f"- {title} at {formatted_time}{location_info}\n"

                return result.strip()
            except Exception as e:
                return f"Error retrieving today's events: {str(e)}"

        return [create_event, get_today_events]

    def initialize(self):
        """Initialize the LLM model and agent executor."""
        # Initialize the model
        try:
            self.model = ChatOpenAI(model=self.model_name)
        except Exception as e:
            print(f"Error initializing ChatOpenAI: {e}")
            return

        # Get calendar tools
        tools = self._get_tools()

        # Create agent with OpenAI Functions agent
        system_message = SystemMessage(content=get_prompt("supervisor"))
        agent = OpenAIFunctionsAgent.from_llm_and_tools(
            llm=self.model, tools=tools, system_message=system_message
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(agent=agent, tools=tools)

    async def process_message(self, user_input: str) -> str:
        """
        Process a user message through the agent.

        Args:
            user_input: The user's message text

        Returns:
            The response from the agent
        """
        try:
            # Run the agent with the user input
            result = await self.agent_executor.ainvoke({"input": user_input})
            return result["output"]

        except Exception as e:
            # Provide a simple fallback if processing fails
            print(f"Processing error: {e}")
            return (
                f"I couldn't process that request properly. Technical detail: {str(e)}"
            )
