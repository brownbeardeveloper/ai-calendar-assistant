from datetime import datetime
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

from calendar_assistant.models.calendar_model import CalendarModel
from calendar_assistant.models.agent_model import Agent
from langchain_openai import ChatOpenAI


class AppController:
    def __init__(self):
        self.calendar = CalendarModel()

        # Initialize agents (if API key is available)
        self.supervisor_agent = None
        self.crud_agent = None
        self._init_agents()

    def _init_agents(self):
        """Initialize the agents if OpenAI API key is available."""
        load_dotenv()  # Load .env file if exists
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key:
            # Use a simpler model to reduce costs during initial development
            model = ChatOpenAI(api_key=api_key, model="gpt-4o-mini")
            self.supervisor_agent = Agent(model=model, agent_type="supervisor")
            self.crud_agent = Agent(model=model, agent_type="crud")

    # Calendar functions
    async def get_events_for_month(self, date: datetime) -> List[Dict[str, Any]]:
        return await self.calendar.get_events_for_month(date)

    async def get_today_events(self) -> List[Dict[str, Any]]:
        return await self.calendar.get_today_events()

    async def process_chat(self, user_input: str) -> str:
        """Processes user input from the chat interface using agents."""
        # If agents aren't initialized, return simple echo response
        if not self.supervisor_agent or not self.crud_agent:
            return f"Agents not initialized (missing API key). Echo: {user_input}"

        try:
            # Step 1: Supervisor agent receives user input
            supervisor_response = self.supervisor_agent.run(user_input)

            # Step 2: Extract supervisor's instruction for CRUD agent
            crud_instruction = f"User asked: '{user_input}'\nSupervisor instruction: {supervisor_response.content}"

            # Step 3: CRUD agent processes instruction
            crud_response = self.crud_agent.run(crud_instruction)

            # Step 4: Supervisor reviews CRUD agent's response
            final_review = (
                f"CRUD agent's response: {crud_response.content}\n\n"
                f"Please provide ONLY the final response to the user. "
                f"Do not include any text like 'Response to User:' or 'Final Response to User:' or any other prefixes. "
                f"Just provide the direct response as if you're speaking to the user."
            )
            final_response = self.supervisor_agent.run(final_review)

            # Extract just the final response content
            # Clean up common prefixes the agent might include
            response_content = final_response.content
            prefixes_to_remove = [
                "Response to User:",
                "Final Response to User:",
                "Final Response:",
                "Response:",
                "To User:",
            ]

            for prefix in prefixes_to_remove:
                if response_content.startswith(prefix):
                    response_content = response_content[len(prefix) :].strip()

            return response_content

        except Exception as e:
            # Provide a simple fallback if agent processing fails
            print(f"Agent processing error: {e}")
            return (
                f"I couldn't process that request properly. Technical detail: {str(e)}"
            )
