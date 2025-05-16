calendar_assistant/
├── main.py                      # Entry point of the application
│
├── config/                      # Configuration management
│   └── constants.py             # Application-wide constants
│
├── core/                        # Core AI logic
│   ├── agent.py                 # AI agent creator
│   ├── agent_tools.py           # Tools used by the AI agent
│   └── supervisor.py            # Supervisor logic for overseeing agent behavior
│
├── ui/                          # User interface components
│   ├── app.py                   # Main application class
│   ├── screens/                 # High-level screen components
│   │   ├── calendar.py          # Calendar screen
│   │   ├── chat.py              # Chat screen
│   │   └── settings.py          # Settings screen
│   └── widgets/                 # Reusable UI widgets
│       ├── calendar_display.py  # Calendar display widget
│       ├── event_list.py        # Event list widget
│       ├── message.py           # Chat message widget
│       └── css.py               # Textual UI styling
│
├── utils/                       # Utility modules
│   ├── helper_class.py          # Syncs agent tools with JSON storage (Google API-ready)
│   ├── chat_helper_class.py     # Handles saving and querying chat without storing memory in GUI
│   └── crud_json.py             # JSON-based CRUD operations