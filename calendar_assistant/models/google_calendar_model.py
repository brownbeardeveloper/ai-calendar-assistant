import os
import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()


class GoogleCalendarModel:
    """
    Model for syncing calendar events with Google Calendar API.
    """

    # Scopes for Google Calendar API
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self):
        self.service = None
        self.credentials = None
        self.credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
        self.token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

        self._initialize_service()

    def _initialize_service(self):
        """Initialize Google Calendar service with authentication."""
        try:
            self.credentials = self._get_credentials()
            if self.credentials:
                self.service = build("calendar", "v3", credentials=self.credentials)
                print("✓ Google Calendar service initialized successfully")
            else:
                print("⚠️  No valid credentials found, service not initialized")

        except Exception as e:
            print(f"Error initializing Google Calendar service: {e}")
            self.service = None

    def _get_credentials(self) -> Optional[Credentials]:
        """Get valid credentials for Google Calendar API."""
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        # If no valid credentials, initiate OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✓ Refreshed expired credentials")
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    creds = None

            if not creds:
                if os.path.exists(self.credentials_file):
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_file, self.SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                        print("✓ Completed OAuth flow")
                    except Exception as e:
                        print(f"Error during OAuth flow: {e}")
                        return None
                else:
                    print(f"Credentials file not found: {self.credentials_file}")
                    return None

            # Save credentials for next run
            if creds:
                with open(self.token_file, "w") as token:
                    token.write(creds.to_json())
                    print("✓ Saved credentials to token file")

        return creds

    def get_calendars(self) -> List[Dict[str, Any]]:
        """Get list of user's calendars."""
        if not self.service:
            print("Google Calendar service not initialized")
            return []

        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = []

            for calendar_item in calendar_list.get("items", []):
                calendars.append(
                    {
                        "id": calendar_item.get("id", ""),
                        "name": calendar_item.get("summary", ""),
                        "description": calendar_item.get("description", ""),
                        "timezone": calendar_item.get("timeZone", ""),
                        "primary": calendar_item.get("primary", False),
                        "access_role": calendar_item.get("accessRole", ""),
                        "color": calendar_item.get("backgroundColor", ""),
                    }
                )

            return calendars

        except HttpError as e:
            print(f"Error getting calendars: {e}")
            return []

    def get_events(
        self,
        calendar_id: str = "primary",
        start_date: str = None,
        end_date: str = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get events from Google Calendar.

        Args:
            calendar_id: Calendar ID (default: 'primary')
            start_date: ISO format start date filter
            end_date: ISO format end date filter
            max_results: Maximum number of events to return
        """
        if not self.service:
            print("Google Calendar service not initialized")
            return []

        try:
            # Set default time range if not provided
            if not start_date:
                start_date = datetime.utcnow().isoformat() + "Z"
            if not end_date:
                end_time = datetime.utcnow() + timedelta(days=30)
                end_date = end_time.isoformat() + "Z"

            events_result = (
                self.service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=start_date,
                    timeMax=end_date,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = []
            for event in events_result.get("items", []):
                converted_event = self._google_event_to_dict(event)
                events.append(converted_event)

            return events

        except HttpError as e:
            print(f"Error getting events: {e}")
            return []

    def create_event(
        self, event_data: Dict[str, Any], calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """
        Create an event in Google Calendar.

        Args:
            event_data: Event data in our local format
            calendar_id: Calendar ID (default: 'primary')
        """
        if not self.service:
            print("Google Calendar service not initialized")
            return {}

        try:
            # Convert to Google Calendar format
            google_event = self._dict_to_google_event(event_data)

            # Create the event
            created_event = (
                self.service.events()
                .insert(calendarId=calendar_id, body=google_event)
                .execute()
            )

            return self._google_event_to_dict(created_event)

        except HttpError as e:
            print(f"Error creating event: {e}")
            return {}

    def update_event(
        self, event_id: str, event_data: Dict[str, Any], calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """Update an existing event in Google Calendar."""
        if not self.service:
            print("Google Calendar service not initialized")
            return {}

        try:
            # Convert to Google Calendar format
            google_event = self._dict_to_google_event(event_data)

            # Update the event
            updated_event = (
                self.service.events()
                .update(calendarId=calendar_id, eventId=event_id, body=google_event)
                .execute()
            )

            return self._google_event_to_dict(updated_event)

        except HttpError as e:
            print(f"Error updating event: {e}")
            return {}

    def delete_event(self, event_id: str, calendar_id: str = "primary") -> bool:
        """Delete an event from Google Calendar."""
        if not self.service:
            print("Google Calendar service not initialized")
            return False

        try:
            self.service.events().delete(
                calendarId=calendar_id, eventId=event_id
            ).execute()
            return True

        except HttpError as e:
            print(f"Error deleting event: {e}")
            return False

    def _dict_to_google_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert our event format to Google Calendar format."""
        google_event = {
            "summary": event_data.get("title", ""),
            "description": event_data.get("description", ""),
        }

        # Handle start time - accept both string and datetime objects
        if event_data.get("start_time"):
            start_time_value = event_data["start_time"]
            if isinstance(start_time_value, str):
                start_dt = datetime.fromisoformat(start_time_value)
            else:
                # Assume it's already a datetime object
                start_dt = start_time_value

            google_event["start"] = {
                "dateTime": start_dt.isoformat(),
                "timeZone": "UTC",
            }

        # Handle end time - accept both string and datetime objects
        if event_data.get("end_time"):
            end_time_value = event_data["end_time"]
            if isinstance(end_time_value, str):
                end_dt = datetime.fromisoformat(end_time_value)
            else:
                # Assume it's already a datetime object
                end_dt = end_time_value

            google_event["end"] = {
                "dateTime": end_dt.isoformat(),
                "timeZone": "UTC",
            }

        # Handle location
        if event_data.get("location"):
            google_event["location"] = event_data.get("location")

        # Handle attendees
        if event_data.get("attendees"):
            attendees_list = []
            attendees_str = event_data.get("attendees", "")
            if attendees_str:
                # Split by comma and create attendee objects
                for email in attendees_str.split(","):
                    email = email.strip()
                    if email:
                        attendees_list.append({"email": email})
                google_event["attendees"] = attendees_list

        return google_event

    def _google_event_to_dict(self, google_event: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Google Calendar event format to our event format."""
        # Extract start and end times
        start_time = ""
        end_time = ""

        if "start" in google_event:
            if "dateTime" in google_event["start"]:
                start_time = google_event["start"]["dateTime"]
            elif "date" in google_event["start"]:
                start_time = google_event["start"]["date"] + "T00:00:00"

        if "end" in google_event:
            if "dateTime" in google_event["end"]:
                end_time = google_event["end"]["dateTime"]
            elif "date" in google_event["end"]:
                end_time = google_event["end"]["date"] + "T00:00:00"

        # Extract attendees
        attendees = ""
        if "attendees" in google_event:
            attendee_emails = [
                attendee.get("email", "") for attendee in google_event["attendees"]
            ]
            attendees = ", ".join(filter(None, attendee_emails))

        return {
            "id": google_event.get("id", ""),
            "title": google_event.get("summary", ""),
            "start_time": start_time,
            "end_time": end_time,
            "description": google_event.get("description", ""),
            "location": google_event.get("location", ""),
            "attendees": attendees,
            "google_id": google_event.get("id", ""),
            "html_link": google_event.get("htmlLink", ""),
        }

    def sync_events_to_google(
        self, local_events: List[Dict[str, Any]], calendar_id: str = "primary"
    ) -> List[Dict[str, Any]]:
        """
        Sync local events to Google Calendar.

        Args:
            local_events: List of events in our local format
            calendar_id: Calendar ID (default: 'primary')

        Returns:
            List of created events with Google IDs
        """
        created_events = []

        for event in local_events:
            try:
                created_event = self.create_event(event, calendar_id)
                if created_event:
                    created_events.append(created_event)
                    print(f"✓ Synced to Google: {event.get('title', '')}")

            except Exception as e:
                print(f"✗ Error syncing event {event.get('title', '')}: {e}")

        return created_events

    def sync_events_from_google(
        self, calendar_id: str = "primary", start_date: str = None, end_date: str = None
    ) -> List[Dict[str, Any]]:
        """
        Sync events from Google Calendar to our local format.

        Args:
            calendar_id: Calendar ID (default: 'primary')
            start_date: ISO format start date filter
            end_date: ISO format end date filter

        Returns:
            List of events in our local format
        """
        try:
            google_events = self.get_events(calendar_id, start_date, end_date)
            print(f"✓ Retrieved {len(google_events)} events from Google Calendar")
            return google_events

        except Exception as e:
            print(f"✗ Error syncing from Google Calendar: {e}")
            return []

    def quick_add_event(
        self, text: str, calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """
        Create an event using Google's Quick Add feature.

        Args:
            text: Natural language event description (e.g., "Lunch tomorrow 12pm")
            calendar_id: Calendar ID (default: 'primary')
        """
        if not self.service:
            print("Google Calendar service not initialized")
            return {}

        try:
            created_event = (
                self.service.events()
                .quickAdd(calendarId=calendar_id, text=text)
                .execute()
            )

            return self._google_event_to_dict(created_event)

        except HttpError as e:
            print(f"Error with quick add: {e}")
            return {}
