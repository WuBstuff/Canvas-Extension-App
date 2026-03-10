from canvasapi import Canvas
from datetime import datetime

class CanvasInterface:
    def __init__(self, token, base_url):
        self.canvas = Canvas(base_url, token)
        self.user = self.canvas.get_current_user()

    def get_calendar_sources(self):
        """
        Returns a list of 'context_codes' for the user and their active courses.
        These are needed to tell the API which calendars to pull data from.
        """
        sources = [f"user_{self.user.id}"] # Always include the personal calendar
        
        # Get active courses to include their assignment calendars
        courses = self.user.get_courses(enrollment_state=['active'])
        for course in courses:
            sources.append(f"course_{course.id}")
            
        return sources

    def get_student_workload(self, start_date, end_date, calendar_ids=None):
        """
        Retrieves assignments from specific calendars. 
        If calendar_ids is None, it defaults to the user's personal calendar.
        """
        if not calendar_ids:
            calendar_ids = [f"user_{self.user.id}"]

        # We must use type='assignment' to get actual graded items
        assignments = self.canvas.get_calendar_events(
            type='assignment',
            start_date=start_date,
            end_date=end_date,
            context_codes=calendar_ids,
            all_events=True
        )
        
        return [{
            "title": getattr(a, 'title', 'Untitled'),
            "due_at": getattr(a, 'start_at', None),
            "points": getattr(a, 'assignment', {}).get('points_possible', 0),
            "context": getattr(a, 'context_name', 'Unknown Course')
        } for a in assignments]

    def get_existing_events(self, start_date, end_date, calendar_ids=None):
        if not calendar_ids:
            calendar_ids = [f"user_{self.user.id}"]

        events = self.canvas.get_calendar_events(
            type='event',
            start_date=start_date,
            end_date=end_date,
            context_codes=calendar_ids,
            all_events=True
        )
        
        return [{
            "title": e.title,
            "start": e.start_at,
            "end": e.end_at,
            "context": getattr(e, 'context_name', 'Personal')
        } for e in events]

    def get_combined_schedule(self, start_date, end_date):
        """
        Retrieves both assignments and events within a specific range.
        start_date/end_date should be strings in YYYY-MM-DD format.
        """
        context_code = f"user_{self.user.id}"

        # # 'type' can be 'event' or 'assignment'
        # # 'undated=False' ensures we only get things with a specific time slot
        # items = self.canvas.get_calendar_events(
        #     all_events=True,
        #     type='event', # You can call this twice, once for 'event' and once for 'assignment'
        #     start_date=start_date,
        #     end_date=end_date,
        #     context_codes=[context_code]
        # )
        # return items

        # The planner belongs to the main canvas object, not self.user
        # Dates must be in ISO format: YYYY-MM-DDTHH:MM:SSZ
        # For simplicity, we just add the time suffix to your date strings
        start = f"{start_date}T00:00:00Z"
        end = f"{end_date}T23:59:59Z"

        items = self.canvas.get_planner_items(start_date=start, end_date=end)
        
        workload = []
        for item in items:
            # Planner items have different attribute names than Calendar events
            # Use .get() or getattr() to avoid crashes if a field is missing
            workload.append({
                "title": getattr(item, 'plannable_title', "Untitled"),
                "due_at": getattr(item, 'plannable_date', "No Date"),
                "course": getattr(item, 'context_name', "General"),
                "points": getattr(item, 'points_possible', 0)
            })
        return workload

    def push_study_block(self, title, start_time, end_time, calendar_id=None):
        """
        Creates a block. If no calendar_id is provided, it defaults to the user's personal calendar.
        """
        target_context = calendar_id if calendar_id else f"user_{self.user.id}"
        
        event_dict = {
            "context_code": target_context,
            "title": title,
            "start_at": start_time,
            "end_at": end_time,
            "description": "Auto-generated study session"
        }
        return self.canvas.create_calendar_event(calendar_event=event_dict)
    
