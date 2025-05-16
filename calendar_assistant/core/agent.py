"""
AI agent creator for the Calendar Assistant.
"""

from calendar_assistant.prompts.agent_prompts import get_prompt


class CalendarAgent:
    """AI agent for calendar management and interaction."""

    def __init__(self, model_name="gpt-4.1-nano", agent_type="supervisor"):
        """Initialize the calendar agent with specified model and agent type."""
        if agent_type not in ["supervisor", "crud"]:
            raise ValueError(
                f"Invalid agent type: {agent_type}. Must be 'supervisor' or 'crud'"
            )

        self.model_name = model_name
        self.agent_type = agent_type
        self.tools = []
        self.system_prompt = get_prompt(agent_type)
        pass

    def add_tool(self, tool):
        """Add a tool to the agent's toolkit."""
        self.tools.append(tool)
        pass

    def create(self):
        """Create and return the AI agent with tools."""
        # Will be implemented with actual LLM integration
        pass

    def run(self, query):
        """Run a query through the agent and return results."""
        # Will be implemented with actual LLM call and response handling
        pass
