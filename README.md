# AI Calendar Assistant version 0.1.0

A modern, intelligent calendar assistant that manages your schedule through natural language interactions with Google Calendar integration.

## Features

- 🗣️ **Natural Language Processing**: Create events using conversational language
- 📅 **Google Calendar Sync**: Full synchronization with Google Calendar
- 🔍 **Smart Event Search**: Find events by date, time, or description
- 🤖 **AI-Powered**: Uses OpenAI for intelligent event parsing
- 🎨 **Modern TUI**: Terminal interface with Textual
- ⚡ **Date Context Aware**: Properly interprets relative dates like "today", "yesterday"

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

3. **Set up Google Calendar**
   ```bash
   python3 scripts/setup_google_calendar.py
   ```

4. **Run the assistant**
   ```bash
   python3 main.py
   ```

## Usage Examples

- "Create a meeting with John tomorrow at 3pm"
- "Schedule lunch with Sarah on Friday at noon"
- "Show me my events for today"
- "What do I have scheduled yesterday?"

## Project Structure

```
ai_calendar/
├── calendar_assistant/
│   ├── config/               # Configuration constants
│   ├── controller/           # Business logic controllers
│   │   └── app_controller.py
│   ├── models/               # Data models & API integrations
│   │   ├── google_calendar_model.py
│   │   └── supervisor_model.py
│   ├── prompts/              # AI agent prompts
│   │   └── agent_prompts.py
│   ├── pytest/              # Internal tests
│   └── ui/                   # Terminal user interface
│       ├── app.py
│       └── widgets/          # UI components
├── scripts/                  # Setup utilities
│   └── setup_google_calendar.py
├── tests/                    # Test suite
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (create this)
```

## Architecture

- **FastAPI-style**: Clean separation of concerns
- **Modern Python**: Type hints, async/await patterns
- **LangChain Agents**: AI-powered calendar operations
- **Google Calendar API**: Real-time synchronization
- **Date Context Injection**: Accurate relative date interpretation

## Dependencies

Core: `openai`, `langchain`, `textual`, `google-api-python-client`, `python-dotenv`

---

Built with Python, OpenAI, and Google Calendar API.