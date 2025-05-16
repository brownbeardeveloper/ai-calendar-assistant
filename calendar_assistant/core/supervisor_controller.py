"""
Supervisor controller for managing communication between supervisor and CRUD agents.
"""

from calendar_assistant.core.agent import CalendarAgent
from calendar_assistant.controllers.calendar_controller import CalendarController
from calendar_assistant.controllers.chat_controller import ChatController


class SupervisorController:
    """Controller for managing supervisor and CRUD agent interactions."""

    def __init__(self, model_name="gpt-4.1-nano"):
        """Initialize the supervisor controller."""
        # Initialize AI agents
        self.supervisor_agent = CalendarAgent(
            model_name=model_name, agent_type="supervisor"
        )
        self.crud_agent = CalendarAgent(model_name=model_name, agent_type="crud")

        # Initialize controllers
        self.calendar_controller = CalendarController()
        self.chat_controller = ChatController()
        pass

    def initialize_agents(self):
        """Initialize both agents with appropriate tools."""
        # Add calendar tools to the CRUD agent
        self._add_calendar_tools()
        pass

    async def process_user_request(self, user_request):
        """Process a user request through the agent system."""
        # Add user message to chat history
        self.chat_controller.add_user_message(user_request)

        # 1. Send user request to supervisor agent
        supervisor_response = await self._run_supervisor(user_request)

        # 2. If supervisor approves/modifies an action, send to CRUD agent
        if self._should_run_crud(supervisor_response):
            crud_instructions = self._extract_crud_instructions(supervisor_response)
            crud_response = await self._run_crud(crud_instructions)

            # 3. Supervisor reviews CRUD result before returning to user
            final_response = await self._supervisor_review(crud_response)

            # Add assistant response to chat history
            self.chat_controller.add_assistant_message(final_response)
            return final_response

        # If no CRUD action needed, return supervisor response directly
        self.chat_controller.add_assistant_message(supervisor_response)
        return supervisor_response
        pass

    async def _run_supervisor(self, user_request):
        """Run the supervisor agent with the user request."""
        # Will implement actual LLM call
        pass

    async def _run_crud(self, instructions):
        """Run the CRUD agent with instructions from the supervisor."""
        # Will implement actual LLM call
        pass

    async def _supervisor_review(self, crud_response):
        """Have supervisor review the CRUD agent's response."""
        # Will implement actual LLM call for final review
        pass

    def _should_run_crud(self, supervisor_response):
        """Determine if CRUD agent should be run based on supervisor response."""
        # Will implement logic to check if supervisor approved an action
        pass

    def _extract_crud_instructions(self, supervisor_response):
        """Extract instructions for the CRUD agent from supervisor response."""
        # Will implement parsing logic
        pass

    def _add_calendar_tools(self):
        """Add calendar operation tools to the CRUD agent."""
        # Create tools that interface with the calendar controller
        # These will be used by the CRUD agent to perform actions
        calendar_tools = [
            {
                "name": "create_event",
                "function": self.calendar_controller.create_event,
                "description": "Create a new calendar event",
            },
            {
                "name": "get_event",
                "function": self.calendar_controller.get_event,
                "description": "Get a calendar event by ID",
            },
            {
                "name": "update_event",
                "function": self.calendar_controller.update_event,
                "description": "Update an existing calendar event",
            },
            {
                "name": "delete_event",
                "function": self.calendar_controller.delete_event,
                "description": "Delete a calendar event",
            },
            {
                "name": "get_events_for_day",
                "function": self.calendar_controller.get_events_for_day,
                "description": "Get all events for a specific day",
            },
            {
                "name": "get_events_for_week",
                "function": self.calendar_controller.get_events_for_week,
                "description": "Get all events for a specific week",
            },
            {
                "name": "search_events",
                "function": self.calendar_controller.search_events,
                "description": "Search for events matching criteria",
            },
            {
                "name": "get_upcoming_events",
                "function": self.calendar_controller.get_upcoming_events,
                "description": "Get upcoming events",
            },
        ]

        # Add tools to the CRUD agent
        for tool in calendar_tools:
            self.crud_agent.add_tool(tool)
        pass
