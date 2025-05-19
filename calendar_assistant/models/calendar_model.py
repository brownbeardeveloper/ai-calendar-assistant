from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional, List
import json
import os
import uuid


class CalendarEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @model_validator(mode="after")
    def check_time_order(self) -> "CalendarEvent":
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        return self


class CalendarModel:
    def __init__(self, storage_file: Optional[str] = None):
        self.storage_file = storage_file or "data/events.json"
        self.events: List[CalendarEvent] = []

    async def load_events(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    raw = json.load(f)
                    self.events = [CalendarEvent(**e) for e in raw]
            return self.events
        except Exception as e:
            print(f"Error loading events: {e}")
            return []

    def save_events(self):
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            with open(self.storage_file, "w") as f:
                json.dump([e.model_dump(mode="json") for e in self.events], f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving events: {e}")
            return False

    def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
    ):
        event = CalendarEvent(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )
        self.events.append(event)
        self.save_events()
        return event

    async def get_events_for_month(self, date: datetime):
        """Return events scheduled in the same year and month as the given date."""
        if not self.events and os.path.exists(self.storage_file):
            await self.load_events()
        filtered_events = [
            e
            for e in self.events
            if e.start_time.year == date.year and e.start_time.month == date.month
        ]
        return [event.model_dump() for event in filtered_events]

    async def get_today_events(self):
        """Return events scheduled for today."""
        if not self.events and os.path.exists(self.storage_file):
            await self.load_events()
        today = datetime.now().date()
        filtered_events = [e for e in self.events if e.start_time.date() == today]
        return [event.model_dump() for event in filtered_events]

    def update_event(self, event_id: str, **update_fields):
        """
        Update an existing calendar event with new field values.

        This method locates the event by its ID, merges the current event data
        with the provided fields, and revalidates the updated event using Pydantic.
        If the updated data violates any model constraints (e.g. start_time >= end_time),
        a ValidationError will be raised.

        Parameters:
            event_id (str): The unique identifier of the event to update.
            **update_fields: Arbitrary keyword arguments corresponding to fields on CalendarEvent
                            (e.g., title, start_time, end_time, description).

        Returns:
            CalendarEvent: The updated event object if found and successfully updated.
            None: If no matching event is found.

        Raises:
            ValidationError: If the updated event data violates model validation rules.
        """
        for i, event in enumerate(self.events):
            if event.id == event_id:
                combined_fields = event.model_dump()
                combined_fields.update(update_fields)
                combined_fields["updated_at"] = datetime.now()
                updated = CalendarEvent(**combined_fields)
                self.events[i] = updated
                self.save_events()
                return updated
        return None

    def delete_event(self, event_id: str):
        for i, event in enumerate(self.events):
            if event.id == event_id:
                deleted = self.events.pop(i)
                self.save_events()
                return deleted
        return None
