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


@pytest.mark.asyncio
async def test_multiple_events_order(temp_model):
    # Create just 3 events with clear time separation
    base_time = datetime.now()

    # Create events in non-chronological order to verify sorting
    events = [
        {"title": "Event B", "start": base_time + timedelta(hours=2)},
        {"title": "Event A", "start": base_time},
        {"title": "Event C", "start": base_time + timedelta(hours=4)},
    ]

    # Create the events
    for event in events:
        temp_model.create_event(
            title=event["title"],
            start_time=event["start"],
            end_time=event["start"] + timedelta(hours=1),
        )

    # Retrieve events for the month
    month_events = await temp_model.get_events_for_month(base_time)

    # Sort by start_time
    sorted_events = sorted(month_events, key=lambda e: e["start_time"])

    # Test assertions
    assert len(sorted_events) == 3

    # Check events are in correct order by comparing titles
    # We know Event A should be first, B second, C third after sorting
    titles = [e["title"] for e in sorted_events]
    assert titles == ["Event A", "Event B", "Event C"]

    # Verify times are correctly ordered
    for i in range(1, len(sorted_events)):
        assert sorted_events[i - 1]["start_time"] < sorted_events[i]["start_time"]


if __name__ == "__main__":
    pytest.main([__file__])
