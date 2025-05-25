# MVC Structured Personal Calendar App with Python's Textual Sync with Google Calendar

![App Screenshot](screenshots/calendar_app.png)

## 💬 Conversation Example & Limits

```bash
User: "Create meeting at 4pm today"
AI: ✅ Created 'Meeting' for today at 4:00 PM

User: "Send invite to john@email.com"  
AI: ✅ Added john@email.com to your meeting at 4:00 PM

User: "Show my calendar"
AI: 📅 Today: Meeting (4:00 PM) 🟢
```

**Limits**: OpenAI API rate limits, Google Calendar API quotas, 10 events max per bulk operation

## 🛠️ Frameworks & Libraries

- **UI**: Python Textual (Terminal UI)
- **AI**: OpenAI GPT + LangChain agents  
- **Calendar**: Google Calendar API
- **Structure**: MVC Pattern

**Use MVC for new repos**: Copy `controller/`, `models/`, `ui/` structure. Replace models with your data layer, keep controller logic, adapt UI widgets.

## 📁 Project Structure

```
ai_calendar/
├── main.py                    # Entry point
├── calendar_assistant/
│   ├── controller/           # MVC Controller
│   │   └── app_controller.py
│   ├── models/              # MVC Model  
│   │   ├── google_calendar_model.py
│   │   └── supervisor_model.py
│   ├── ui/                  # MVC View
│   │   ├── app.py           # Main UI app
│   │   └── widgets/calendar_display.py
│   └── prompts/             # AI system prompts
└── scripts/                 # Setup utilities
```

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup Google Calendar API
python scripts/setup_google_calendar.py

# 3. Create .env file with your API keys
# .env should contain:
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# 4. Run
python main.py
```

## 🎯 Features

- 🤖 **Conversational AI**: Natural language → calendar events
- 🎨 **Visual Calendar**: Color-coded event density  
- 🚦 **Conflict Detection**: Prevents double-booking
- 🔒 **Security**: Audit trails, confirmation prompts
- 📅 **Google Sync**: Real-time calendar synchronization
- 🕐 **Timezone Aware**: Handles global scheduling

**Perfect for**: Personal productivity, AI calendar automation, terminal-based workflow integration.