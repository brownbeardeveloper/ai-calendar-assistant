import os
import pytest
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from calendar_assistant.models.agent_model import Agent

load_dotenv()


@pytest.fixture(scope="module")
def real_agent():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        pytest.fail("OPENAI_API_KEY not found in .env")

    model = ChatOpenAI(api_key=api_key, model="gpt-4.1-nano")
    return Agent(model=model, agent_type="crud")


def test_agent_real_run(real_agent):
    response = real_agent.run("Create a meeting with Alice at 14:00 tomorrow.")

    assert hasattr(response, "content")
    assert isinstance(response.content, str)
    assert len(response.content.strip()) > 0


if __name__ == "__main__":
    pytest.main([__file__])
