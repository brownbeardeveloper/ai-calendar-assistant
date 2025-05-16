"""
Textual UI styling for the Calendar Assistant.
"""

# Main application styles
APP_CSS = """
CalendarApp {
    background: $surface;
}

Screen {
    padding: 1 2;
}
"""

# Calendar screen specific styles
CALENDAR_CSS = """
CalendarDisplay {
    width: 100%;
    height: 70%;
    border: solid $primary;
}

EventList {
    width: 100%;
    height: 30%;
    border: solid $primary;
}
"""

# Chat screen specific styles
CHAT_CSS = """
MessageWidget {
    margin: 1 0;
    padding: 1 2;
    border-radius: 1;
}

MessageWidget.user {
    background: $primary-darken-1;
    color: $text;
}

MessageWidget.assistant {
    background: $primary-lighten-1;
    color: $text;
}
"""

# Settings screen specific styles
SETTINGS_CSS = """
SettingsScreen {
    layout: grid;
    grid-size: 2;
    grid-gutter: 1 2;
    padding: 1;
}
"""


def get_combined_css():
    """Get combined CSS styles for the application."""
    return "\n".join([APP_CSS, CALENDAR_CSS, CHAT_CSS, SETTINGS_CSS])
    pass
