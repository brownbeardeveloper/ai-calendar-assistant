"""
Calendar display widget for the Calendar Assistant UI.
"""

from datetime import datetime, timedelta
from calendar import monthrange
from textual.widgets import Static
from textual.containers import Grid
from rich.table import Table
from rich.text import Text


class CalendarDisplay(Static):
    """Widget for displaying a calendar view."""

    def __init__(self, events=None, date=None):
        """Initialize the calendar display."""
        super().__init__()
        self.current_date = date or datetime.now()
        self.view_type = "month"  # month, week, day
        self.events = events or []
        self.highlighted_events = {}

    def on_mount(self):
        """Handle the widget mount event."""
        self.border_title = f"Calendar - {self.current_date.strftime('%B %Y')}"
        self.update()

    def render(self):
        """Render the calendar display."""
        if self.view_type == "month":
            return self._render_month_view()
        # Add support for other views later
        return Text("Calendar view not implemented")

    def _render_month_view(self):
        """Render a month view calendar."""
        table = Table(expand=True)

        # Add day headers
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            table.add_column(day, justify="center")

        # Get first day of month and number of days
        year, month = self.current_date.year, self.current_date.month
        first_day = datetime(year, month, 1)
        _, num_days = monthrange(year, month)

        # Calculate the weekday of the first day (0 is Monday in our display)
        first_weekday = first_day.weekday()

        # Generate the calendar grid
        day = 1
        for week in range(6):  # Max 6 weeks in a month view
            row = []
            for weekday in range(7):
                if (week == 0 and weekday < first_weekday) or day > num_days:
                    # Empty cell
                    row.append("")
                else:
                    # Date cell
                    date_text = Text(str(day))

                    # Highlight current day
                    is_today = (
                        day == datetime.now().day
                        and month == datetime.now().month
                        and year == datetime.now().year
                    )

                    if is_today:
                        date_text.stylize("bold reverse")

                    # Check for events on this day
                    day_events = self._get_events_for_day(year, month, day)
                    if day_events:
                        if is_today:
                            date_text.stylize("bold reverse blue")
                        else:
                            date_text.stylize("bold blue")

                    row.append(date_text)
                    day += 1

            # Only add the row if it has at least one date
            if any(cell != "" for cell in row):
                table.add_row(*row)

        return table

    def _get_events_for_day(self, year, month, day):
        """Get events for a specific day."""
        day_start = datetime(year, month, day).isoformat()
        day_end = (
            datetime(year, month, day) + timedelta(days=1) - timedelta(microseconds=1)
        ).isoformat()

        return [
            e
            for e in self.events
            if e.get("start_time", "") >= day_start
            and e.get("start_time", "") <= day_end
        ]

    def set_view(self, view_type):
        """Set the calendar view type."""
        if view_type in ["month", "week", "day"]:
            self.view_type = view_type
            self.update()

    def navigate(self, direction):
        """Navigate the calendar in a direction (prev, next)."""
        if self.view_type == "month":
            if direction == "prev":
                # Go to previous month
                if self.current_date.month == 1:
                    self.current_date = self.current_date.replace(
                        year=self.current_date.year - 1, month=12
                    )
                else:
                    self.current_date = self.current_date.replace(
                        month=self.current_date.month - 1
                    )
            else:
                # Go to next month
                if self.current_date.month == 12:
                    self.current_date = self.current_date.replace(
                        year=self.current_date.year + 1, month=1
                    )
                else:
                    self.current_date = self.current_date.replace(
                        month=self.current_date.month + 1
                    )

            self.border_title = f"Calendar - {self.current_date.strftime('%B %Y')}"
            self.update()

    def highlight_events(self, events):
        """Highlight events on the calendar."""
        self.events = events
        self.update()
