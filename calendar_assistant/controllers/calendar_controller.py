"""
Calendar controller for the Calendar Assistant.
Handles interactions between UI and calendar data model.
"""

from calendar_assistant.models.calendar_model import CalendarModel
from datetime import datetime, timedelta


class CalendarController:
    """Controller for managing calendar operations."""

    def __init__(self, model=None):
        """Initialize the calendar controller with a model."""
        self.model = model or CalendarModel()
        self.model.load_events()
        pass

    def create_event(self, title, start_time, end_time, description=None):
        """Create a new calendar event."""
        # Validate inputs
        if not title:
            return {"success": False, "error": "Event title is required"}

        try:
            # Convert string times to datetime if needed
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time)
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time)

            # Validate times
            if end_time <= start_time:
                return {"success": False, "error": "End time must be after start time"}

            # Convert back to ISO format strings for storage
            start_iso = start_time.isoformat()
            end_iso = end_time.isoformat()

            # Create the event
            event = self.model.create_event(title, start_iso, end_iso, description)
            return {"success": True, "event": event}

        except Exception as e:
            return {"success": False, "error": str(e)}
        pass

    def get_event(self, event_id):
        """Get a calendar event by ID."""
        event = self.model.get_event(event_id)
        if event:
            return {"success": True, "event": event}
        return {"success": False, "error": "Event not found"}
        pass

    def update_event(self, event_id, **update_fields):
        """Update a calendar event."""
        # Validate that event exists
        if not self.model.get_event(event_id):
            return {"success": False, "error": "Event not found"}

        try:
            # Handle time conversions
            if "start_time" in update_fields and isinstance(
                update_fields["start_time"], datetime
            ):
                update_fields["start_time"] = update_fields["start_time"].isoformat()
            if "end_time" in update_fields and isinstance(
                update_fields["end_time"], datetime
            ):
                update_fields["end_time"] = update_fields["end_time"].isoformat()

            # Update the event
            updated_event = self.model.update_event(event_id, **update_fields)
            return {"success": True, "event": updated_event}

        except Exception as e:
            return {"success": False, "error": str(e)}
        pass

    def delete_event(self, event_id):
        """Delete a calendar event."""
        deleted_event = self.model.delete_event(event_id)
        if deleted_event:
            return {"success": True, "event": deleted_event}
        return {"success": False, "error": "Event not found"}
        pass

    def get_events_for_day(self, date=None):
        """Get all events for a specific day."""
        if date is None:
            date = datetime.now()

        # Set start and end of day
        start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0).isoformat()
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59).isoformat()

        # Query events for the day
        events = self.model.query_events(start_date=start_of_day, end_date=end_of_day)
        return {"success": True, "events": events}
        pass

    def get_events_for_week(self, date=None):
        """Get all events for a specific week."""
        if date is None:
            date = datetime.now()

        # Calculate start and end of week
        start_of_week = (
            (date - timedelta(days=date.weekday()))
            .replace(hour=0, minute=0, second=0)
            .isoformat()
        )
        end_of_week = (
            (date + timedelta(days=6 - date.weekday()))
            .replace(hour=23, minute=59, second=59)
            .isoformat()
        )

        # Query events for the week
        events = self.model.query_events(start_date=start_of_week, end_date=end_of_week)
        return {"success": True, "events": events}
        pass

    def search_events(self, query, start_date=None, end_date=None):
        """Search for events matching criteria."""
        events = self.model.query_events(
            query=query, start_date=start_date, end_date=end_date
        )
        return {"success": True, "events": events, "count": len(events)}
        pass

    def get_upcoming_events(self, limit=5):
        """Get upcoming events from now."""
        now = datetime.now().isoformat()

        # Get all future events
        future_events = self.model.query_events(start_date=now)

        # Sort by start time
        sorted_events = sorted(future_events, key=lambda e: e.get("start_time", ""))

        # Return limited number
        limited_events = sorted_events[:limit] if limit else sorted_events
        return {"success": True, "events": limited_events}
        pass
