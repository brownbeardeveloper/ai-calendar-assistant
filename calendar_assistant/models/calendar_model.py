"""
Calendar data model for the Calendar Assistant.
Handles data storage and CRUD operations for calendar events.
"""

import json
import os
import uuid
from pathlib import Path
from datetime import datetime


class CalendarModel:
    """Model for calendar data storage and operations."""

    def __init__(self, storage_file=None):
        """Initialize the calendar model with storage file path."""
        self.storage_file = storage_file or "data/calendar_data.json"
        self.events = []
        pass

    def load_events(self):
        """Load events from storage."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    self.events = json.load(f)
            return self.events
        except Exception as e:
            print(f"Error loading events: {e}")
            return []
        pass

    def save_events(self):
        """Save events to storage."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)

            with open(self.storage_file, "w") as f:
                json.dump(self.events, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving events: {e}")
            return False
        pass

    def create_event(self, title, start_time, end_time, description=None):
        """Create a new calendar event."""
        event_id = str(uuid.uuid4())
        event = {
            "id": event_id,
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "description": description,
            "created_at": datetime.now().isoformat(),
        }

        self.events.append(event)
        self.save_events()
        return event
        pass

    def get_event(self, event_id):
        """Get a calendar event by ID."""
        for event in self.events:
            if event.get("id") == event_id:
                return event
        return None
        pass

    def update_event(self, event_id, **update_fields):
        """Update a calendar event."""
        for i, event in enumerate(self.events):
            if event.get("id") == event_id:
                # Update the event with new fields
                self.events[i] = {
                    **event,
                    **update_fields,
                    "updated_at": datetime.now().isoformat(),
                }
                self.save_events()
                return self.events[i]
        return None
        pass

    def delete_event(self, event_id):
        """Delete a calendar event."""
        for i, event in enumerate(self.events):
            if event.get("id") == event_id:
                deleted_event = self.events.pop(i)
                self.save_events()
                return deleted_event
        return None
        pass

    def query_events(self, query=None, start_date=None, end_date=None):
        """Query events based on search parameters."""
        results = []

        for event in self.events:
            # Start with True and apply filters
            matches = True

            if query:
                # Check if query is in title or description
                title = event.get("title", "").lower()
                description = event.get("description", "").lower()
                if query.lower() not in title and query.lower() not in description:
                    matches = False

            if start_date and event.get("start_time"):
                if event.get("start_time") < start_date:
                    matches = False

            if end_date and event.get("end_time"):
                if event.get("end_time") > end_date:
                    matches = False

            if matches:
                results.append(event)

        return results
        pass
