"""
CSS styles for the Calendar Assistant UI.
"""

CSS = """
/* Layout styles */
#chat-section, #calendar-section {
    width: 1fr;
    height: 100%;
}

.column {
    padding: 1;
    height: 100%;
}

/* Chat container styles */
#chat-container {
    height: 1fr;
    overflow-y: auto;
    padding: 1;
    border: solid $primary;
    border-top: solid $primary;
    border-right: solid $primary;
    border-left: solid $primary;
    border-bottom: none;
    layout: vertical;
}

#chat-input {
    height: 3;
    margin: 0 1;
    border: solid $primary;
}

/* Calendar styles */
CalendarDisplay {
    height: 60%;
    border: solid $primary;
    margin: 0 0 1 0;
}

EventList {
    height: 40%;
    border: solid $primary;
}

/* Special styling for user/assistant messages */
.user {
    width: 80%;
    margin: 1;
    align: right middle;
    display: block;
}

.assistant {
    width: 80%;
    margin: 1;
    align: left middle;
    display: block;
}

/* Tab styles */
#tabs {
    dock: top;
    height: 3;
    padding: 0 1;
    background: $surface;
}

.tab {
    padding: 0 2;
    height: 3;
    border-bottom: solid $primary;
}

.tab-active {
    border-bottom: solid $accent;
    color: $accent;
    text-style: bold;
}

.tab-inactive {
    border-bottom: solid $primary-darken-1;
    color: $text-muted;
}

/* Tab content styles */
#calendar-tab-content, #chat-tab-content, #gui-tab-content {
    height: 100%;
}

/* Calendar layout in calendar tab */
#calendar-layout {
    layout: horizontal;
    height: 100%;
}

#calendar-view {
    width: 2fr;
    height: 100%;
}

#today-events {
    width: 1fr;
    height: 100%;
}

/* Hidden elements */
.hidden {
    display: none;
}

/* Chat content area */
#chat-content {
    height: 100%;
    overflow-y: auto;
}

/* Make sure chat container fills available space */
#chat-tab-content {
    height: 100%;
    overflow: hidden;
}
"""
