from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
from calendar_assistant.models.calendar_model import CalendarModel, CalendarEvent
import os
import tempfile
import pytest
import asyncio


@pytest.fixture
def temp_model():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    model = CalendarModel(storage_file=path)
    yield model
    os.remove(path)


def test_create_invalid_time_order(temp_model):
    start = datetime.now()
    end = start - timedelta(minutes=30)  # invalid

    with pytest.raises(ValidationError):
        temp_model.create_event("Invalid Time", start, end)


def test_create_missing_title(temp_model):
    start = datetime.now()
    end = start + timedelta(hours=1)

    with pytest.raises(ValidationError):
        CalendarEvent(start_time=start, end_time=end)  # no title


def test_create_and_reload(temp_model):
    start = datetime.now()
    end = start + timedelta(minutes=30)
    temp_model.create_event("Persistent", start, end)

    reloaded_model = CalendarModel(storage_file=temp_model.storage_file)
    events = asyncio.run(reloaded_model.load_events())

    assert isinstance(events, list)
    assert len(events) == 1
    assert events[0].title == "Persistent"


def test_timezone_aware_event(temp_model):
    tz = timezone.utc
    start = datetime(2025, 5, 20, 10, 0, tzinfo=tz)
    end = datetime(2025, 5, 20, 11, 0, tzinfo=tz)

    event = temp_model.create_event("UTC Event", start, end)
    assert event.start_time.tzinfo == timezone.utc


def test_update_event_with_invalid_time(temp_model):
    now = datetime.now()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    event = temp_model.create_event("Update Target", start, end)

    with pytest.raises(ValidationError):
        temp_model.update_event(
            event.id, start_time=end + timedelta(hours=1), end_time=start
        )


def test_multiple_events_order(temp_model):
    base = datetime.now() + timedelta(minutes=1)
    for i in range(5):
        temp_model.create_event(
            title=f"Event {i}",
            start_time=base + timedelta(hours=i * 2),
            end_time=base + timedelta(hours=i * 2 + 1),
        )

    upcoming = temp_model.get_upcoming_events()
    assert len(upcoming) == 5
    assert upcoming[0].start_time < upcoming[1].start_time


if __name__ == "__main__":
    pytest.main([__file__])
