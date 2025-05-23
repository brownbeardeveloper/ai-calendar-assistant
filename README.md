# AI Calendar Assistant

A terminal-based calendar assistant powered by AI that helps you manage your schedule through natural language.

## Project Structure

```markdown
ai_calendar/
├── main.py                      # Entry point of the application
│
├── calendar_assistant/          # Main package
│   ├── config/                  # Configuration management
│   │   └── constants.py         # Application-wide constants
│   │
│   ├── controller/              # Business logic (C in MVC)
│   │   └── app_controller.py    # Main application controller
│   │
│   ├── models/                  # Data models (M in MVC)
│   │   ├── agent_model.py       # AI agent definition
│   │   └── calendar_model.py    # Calendar data storage and operations
│   │
│   ├── tools/                   # Tools used by the AI agent
│   │   └── agent_tools.py       # Implementation of agent tools
│   │
│   ├── prompts/                 # AI prompt templates
│   │   └── agent_prompts.py     # Prompts for different agent types
│   │
│   ├── pytest/                  # Test suite
│   │   ├── test_calendar_model.py # Tests for calendar functionality
│   │   ├── test_agent_model.py  # Tests for agent functionality
│   │   └── pytest.ini           # Pytest configuration
│   │
│   └── ui/                      # User interface components (V in MVC)
│       ├── app.py               # Main application UI class
│       └── widgets/             # Reusable UI components
│           ├── calendar_display.py # Calendar display widget
│           ├── event_list.py    # Event list widget
│           ├── message.py       # Chat message widget
│           └── css.py           # Textual UI styling
│
├── data/                        # Data storage
│   └── events.json              # Calendar events storage
│
└── requirements.txt             # Project dependencies
```

## Features

- Natural language interface for managing calendar events
- Terminal-based UI using Textual
- AI-powered understanding of date/time expressions
- Event creation, modification, and deletion

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set your OpenAI API key: `export OPENAI_API_KEY=your_key_here`
4. Run the application: `python main.py`

## Usage

Use natural language to interact with your calendar:
- "Create a meeting with John tomorrow at 2pm"
- "Show me my schedule for next week"
- "Cancel my 3pm appointment"

## Requirements

- Python 3.8+
- OpenAI API key

## Testing

To run the tests, use the following command:
```
pytest calendar_assistant/pytest/
```