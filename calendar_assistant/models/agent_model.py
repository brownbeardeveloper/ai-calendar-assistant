"""
AI agent creator.
"""

from calendar_assistant.prompts.agent_prompts import get_prompt
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class Agent:
    def __init__(self, model: ChatOpenAI, agent_type: str):
        self.model = model
        self.agent_type = agent_type  # "supervisor" or "crud"
        self.tools = []
        self.system_prompt = get_prompt(agent_type)

    def add_tool(self, tool):
        self.tools.append(tool)

    def run(self, query: str):
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=query),
        ]
        return self.model.invoke(messages)
