"""
CSS styles for the Calendar Assistant UI.
"""

CSS = """
#chat-section, #calendar-section {
    width: 1fr;
    height: 100%;
}

.column {
    padding: 1;
    height: 100%;
}

#chat-container {
    height: 1fr;
    overflow-y: auto;
    padding: 1;
    border: solid $primary;
    border-top: solid $primary;
    border-right: solid $primary;
    border-left: solid $primary;
    border-bottom: none;
}

#chat-input {
    height: 3;
    margin: 0 1;
    border: solid $primary;
}

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
    margin: 1;
    width: 80%;
    align-horizontal: right;
}

.assistant {
    margin: 1;
    width: 80%;
    align-horizontal: left;
}
"""
