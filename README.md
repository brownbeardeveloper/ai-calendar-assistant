calendar_assistant/
├── main.py                      # Entry point of the application
│
├── config/                      # Configuration management
│   └── constants.py             # Application-wide constants
│
├── models/                      # Data models (M in MVC)
│   ├── calendar_model.py        # Calendar data storage and operations
│   ├── chat_model.py            # Chat history data storage and operations
│   └── settings_model.py        # Application settings storage
│
├── controllers/                 # Business logic (C in MVC)
│   ├── calendar_controller.py   # Calendar operations controller
│   ├── chat_controller.py       # Chat operations controller
│   └── settings_controller.py   # Settings operations controller
│
├── core/                        # Core AI logic
│   ├── agent.py                 # AI agent creator
│   ├── agent_tools.py           # Tools used by the AI agent
│   ├── supervisor.py            # Supervisor logic for agent behavior
│   └── supervisor_controller.py # Controller for supervisor and CRUD agents
│
├── ui/                          # User interface components (V in MVC)
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
├── prompts/                     # AI prompt templates
│   └── agent_prompts.py         # Prompts for different agent types
│
└── utils/                       # Utility functions and helpers