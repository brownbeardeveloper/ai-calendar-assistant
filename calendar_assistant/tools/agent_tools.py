from langchain_core.tools import tool
from calendar_assistant.models.calendar_model import CalendarModel
from datetime import datetime


@tool
def create_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str,
    model: CalendarModel,
):
    """
    Create a new calendar event.

    Args:
        title: Event title
        start_time: ISO format start time (e.g. 2025-05-20T10:00)
        end_time: ISO format end time (e.g. 2025-05-20T11:00)
        description: Optional description
    """
    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        event = model.create_event(title, start, end, description)
        return f"Created event: '{event.title}' from {event.start_time} to {event.end_time}"
    except Exception as e:
        return f"Error creating event: {str(e)}"


@tool
def get_today_events(model: CalendarModel = None):
    """
    List all events scheduled for today.
    """
    events = model.get_today_events()
    if not events:
        return "No events for today."
    return "\n".join(f"- {e.title} at {e.start_time.strftime('%H:%M')}" for e in events)


@tool
def get_upcoming_events(model: CalendarModel = None):
    """
    List all upcoming events.
    """
    events = model.get_upcoming_events()
    if not events:
        return "No events for today."
    return "\n".join(f"- {e.title} at {e.start_time.strftime('%H:%M')}" for e in events)
