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
        # Maps high-point assignments into the free slots
        return list_of_suggested_events
