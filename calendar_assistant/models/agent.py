"""
AI agent creator.
"""

from calendar_assistant.prompts.agent_prompts import get_prompt
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os


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


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OpenAI API key in the .env file.")

    model = ChatOpenAI(api_key=api_key, model="gpt-4.1-nano")
    agent = Agent(model=model, agent_type="crud")
    response = agent.run("Create a meeting tomorrow at 10am with Ben")
    print(f"Response: {response.content}")
