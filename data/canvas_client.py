from canvasapi import Canvas
from datetime import datetime

class CanvasInterface:
    def __init__(self, token, base_url):
        self.canvas = Canvas(base_url, token)
        self.user = self.canvas.get_current_user()

    def get_calendar_sources(self):
        """
        Returns a list of dictionaries containing the Name and ID of favorite calendars.
        """
        # Start with the personal calendar
        sources = [{"name": "Personal Calendar", "id": f"user_{self.user.id}"}]
        
        # Get favorite courses (the ones on their dashboard/calendar tab)
        favorites = self.user.get_favorite_courses()
        
        for course in favorites:
            # Some favorites might be old or weird shells, 
            # but the 'Favorite' status is our best filter.
            name = getattr(course, 'name', f"Course {course.id}")
            sources.append({"name": name, "id": f"course_{course.id}"})
                
        return sources
    
    def get_course_weights(self, calendar_id):
        """
        Takes a calendar ID (e.g., 'course_12345') and returns a dictionary
        of assignment groups and their percentage weights.
        """
        # 1. Strip the 'course_' prefix to get the raw integer ID
        try:
            course_id = int(calendar_id.replace("course_", ""))
        except ValueError:
            return {"Error": "Invalid Course ID format"}

        try:
            course = self.canvas.get_course(course_id)
            
            # Check if the course actually uses weighted grading
            if not getattr(course, "apply_assignment_group_weights", False):
                return {"Grading Type": "Points-based (No weights applied)"}

            # 2. Fetch all assignment groups for this course
            assignment_groups = course.get_assignment_groups()
            
            # 3. Construct the weight dictionary
            # Canvas stores weights as floats (e.g., 20.0 represents 20%)
            weights = {
                group.name: f"{group.group_weight}%" 
                for group in assignment_groups 
                if group.group_weight > 0
            }
            
            return weights if weights else {"Grading": "No weighted groups found"}
            
        except Exception as e:
            return {"Error": f"Could not retrieve weights: {str(e)}"}

    def get_student_workload(self, start_date, end_date, calendar_ids=None):
        if not calendar_ids:
            calendar_ids = [f"user_{self.user.id}"]

        # Force the time to cover the full range of the days provided
        # Format: 2026-02-25T00:00:00Z
        iso_start = f"{start_date}T00:00:00Z"
        iso_end = f"{end_date}T23:59:59Z"

        workload = []
        for code in calendar_ids:
            try:
                items = self.canvas.get_calendar_events(
                    type='assignment',
                    start_date=iso_start,
                    end_date=iso_end,
                    context_codes=[code],
                    all_events=True
                )
                
                for a in items:
                    # Double-check: Canvas sometimes returns items slightly outside range
                    # depending on the 'updated_at' vs 'due_at' logic.
                    workload.append({
                        "title": getattr(a, 'title', 'Untitled'),
                        "due_at": getattr(a, 'start_at', None),
                        "points": getattr(a, 'assignment', {}).get('points_possible', 0),
                        "context": getattr(a, 'context_name', 'Unknown')
                    })
            except Exception:
                continue
                
        return workload
        # """
        # Retrieves assignments from specific calendars. 
        # If calendar_ids is None, it defaults to the user's personal calendar.
        # """
        # if not calendar_ids:
        #     calendar_ids = [f"user_{self.user.id}"]

        # # We must use type='assignment' to get actual graded items
        # assignments = self.canvas.get_calendar_events(
        #     type='assignment',
        #     start_date=start_date,
        #     end_date=end_date,
        #     context_codes=calendar_ids,
        #     all_events=True
        # )
        
        # return [{
        #     "title": getattr(a, 'title', 'Untitled'),
        #     "due_at": getattr(a, 'start_at', None),
        #     "points": getattr(a, 'assignment', {}).get('points_possible', 0),
        #     "context": getattr(a, 'context_name', 'Unknown Course')
        # } for a in assignments]

    def get_existing_events(self, start_date, end_date, calendar_ids=None):
        if not calendar_ids:
            calendar_ids = [f"user_{self.user.id}"]

        # Force the time to cover the full range of the days provided
        # Format: 2026-02-25T00:00:00Z
        iso_start = f"{start_date}T00:00:00Z"
        iso_end = f"{end_date}T23:59:59Z"

        all_events = []

        for code in calendar_ids:
            try:
                events = self.canvas.get_calendar_events(
                    type='event',
                    start_date=iso_start,
                    end_date=iso_end,
                    context_codes=[code],
                    all_events=True
                )
                for e in events:
                    all_events.append({
                        "title": e.title,
                        "start": e.start_at,
                        "end": e.end_at,
                        "context": getattr(e, 'context_name', 'Personal')
                    })
            except Exception as e:
                print(f"Skipping calendar {code} due to error: {e}")
                continue
                
        return all_events
        # if not calendar_ids:
        #     calendar_ids = [f"user_{self.user.id}"]

        # events = self.canvas.get_calendar_events(
        #     type='event',
        #     start_date=start_date,
        #     end_date=end_date,
        #     context_codes=calendar_ids,
        #     all_events=True
        # )
        
        # return [{
        #     "title": e.title,
        #     "start": e.start_at,
        #     "end": e.end_at,
        #     "context": getattr(e, 'context_name', 'Personal')
        # } for e in events]

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
    
