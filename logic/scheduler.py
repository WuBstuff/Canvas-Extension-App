from datetime import datetime, timedelta

class SmartScheduler:
    def __init__(self, assignments, existing_events):
        """
        assignments: List of dicts including 'name', 'due_at', 'points', 
                     and 'group_weight' (e.g., 20 for 20%)
        existing_events: List of (start, end) datetime tuples
        """
        self.assignments = assignments
        self.busy_blocks = sorted(existing_events)

    def find_free_slots(self, day_start, day_end):
        freetime = []
        current_time = day_start

        valid_blocks = sorted([
            (max(day_start, s), min(day_end, e))
            for s, e in self.busy_blocks if s < day_end and e > day_start
        ])

        for start, end in valid_blocks:
            if start > current_time:

                if (start - current_time) >= timedelta(minutes=30):
                    freetime.append((current_time, start))
            current_time = max(current_time, end)
        
        if current_time < day_end:
            freetime.append((current_time, day_end))
        
        return freetime

    def generate_predictions(self):
        suggested_events = []

        now = datetime.now()
        
        for task in self.assignments:
            weight = task.get('group_weight', 1)
            time_diff = (task['due_at'] - now).total_seconds() / 3600
            
            hours_left = max(1, time_diff)
            
            task['priority_score'] = (task['points'] * weight) / hours_left

        sorted_tasks = sorted(self.assignments, key=lambda x: x['priority_score'], reverse=True)

        horizon = now + timedelta(days=3)
        free_slots = self.find_free_slots(now, horizon)

        slot_index = 0
        for task in sorted_tasks:

            if slot_index < len(free_slots):
                start, end = free_slots[slot_index]
                
                if start < task['due_at']:

                    study_duration = min(2, max(1, task['points'] / 50))
                    
                    suggested_events.append({
                        "title": f"📝 High Priority: {task['name']}",
                        "start_at": start.isoformat(),
                        "end_at": (start + timedelta(hours=study_duration)).isoformat(),
                        "description": f"Priority Score: {round(task['priority_score'], 2)}"
                    })
                    slot_index += 1
        
        return suggested_events
