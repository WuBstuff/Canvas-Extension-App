from datetime import datetime

class CanvasInterface:
    def __init__(self, token, base_url):
        self.canvas = Canvas(base_url, token)
        self.user = self.canvas.get_current_user()

    def get_student_workload(self, start_date, end_date):
        # This pulls assignments appearing on the calendar in this window
        assignments = self.canvas.get_calendar_events(
            type='assignment',
            start_date=start_date,
            end_date=end_date,
            context_codes=[f"user_{self.user.id}"]
        )
        
        return [{
            "title": a.title,
            "due_at": a.start_at, # For assignments, start_at is the due date
            "points": getattr(a, 'assignment', {}).get('points_possible', 0)
        } for a in assignments]

    def get_existing_events(self, start_date, end_date):
        events = self.canvas.get_calendar_events(
            type='event',
            start_date=start_date,
            end_date=end_date,
            context_codes=[f"user_{self.user.id}"]
        )
        
        return [{
            "title": e.title,
            "start": e.start_at,
            "end": e.end_at
        } for e in events]

    def get_combined_schedule(self, start_date, end_date):
        """
        Retrieves both assignments and events within a specific range.
        start_date/end_date should be strings in YYYY-MM-DD format.
        """
        context_code = f"user_{self.user.id}"
        
        # 'type' can be 'event' or 'assignment'
        # 'undated=False' ensures we only get things with a specific time slot
        items = self.canvas.get_calendar_events(
            all_events=True,
            type='event', # You can call this twice, once for 'event' and once for 'assignment'
            start_date=start_date,
            end_date=end_date,
            context_codes=[context_code]
        )
        return items

    def push_study_block(self, title, start_time, end_time):
        # The API expects a dict of event attributes
        event_dict = {
            "context_code": f"user_{self.user.id}",
            "title": title,
            "start_at": start_time, # Must be ISO 8601 string (e.g., "2026-02-16T15:00:00Z")
            "end_at": end_time,
            "description": "Auto-generated study session"
        }
        
        return self.canvas.create_calendar_event(calendar_event=event_dict)
