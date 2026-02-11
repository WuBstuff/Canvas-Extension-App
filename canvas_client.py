class CanvasInterface:
    def __init__(self, token, base_url):
        self.canvas = Canvas(base_url, token)
        self.user = self.canvas.get_current_user()

    def get_student_workload(self):
        # Returns a list of assignment objects with due dates & points
        pass

    def get_existing_events(self):
        # Returns a list of calendar events to identify "blocked" time
        pass

    def push_study_block(self, title, start_time, end_time):
        # Creates the POST request to the Canvas Calendar
        pass
