class SmartScheduler:
    def __init__(self, assignments, existing_events):
        self.assignments = assignments
        self.calendar = existing_events

    def find_free_slots(busy_blocks, day_start, day_end):
        # get time blocks from start of the day to end of the day and sort them
        busy_blocks.sort()
        valid_blocks = [(max(day_start, s), min(day_end, e))
            for s, e in busy_blocks if s < day_end and e > day_start]
        freetime = []
        current_time = day_start

        # find times that are available
        for start, end in valid_blocks:
            if start > current_time:
                freetime.append((current_time, start))
            current_time = max(current_time, end)
        
        # check for last event on occasion there is more time after
        if current_time < day_end:
            freetime.append((current_time, day_end))
        
        return freetime


    def generate_predictions(self):
        suggested_events = []
        # sort by importance
        sorted_tasks = sorted(self.assignments, key=lambda x: x['due_at'])

        # time slot for 3 days place holder
        now = datetime.now()
        horizon = now + timedelta(days=3)
        free_slots = self.find_free_slots(now, horizon)

        slot_index = 0
        for task in sorted_tasks:
            if slot_index < len(free_slots):
                start, end = free_slots[slot_index]
                
                suggested_events.append({
                    "title": f"📝 Study: {task['name']}",
                    "start_at": start.isoformat(),
                    "end_at": (start + timedelta(hours=1)).isoformat()
                })
                slot_index += 1
        
        return suggested_events
