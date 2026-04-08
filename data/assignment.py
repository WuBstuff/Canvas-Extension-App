#This file holds the Assignment class, which outlines how Assignments are stored and changed, subject to change

from datetime import datetime, timedelta

def round_to_nearest_minute(dt):
    # Round down to the nearest minute by stripping seconds/microseconds
    rounded_dt = dt.replace(second=0, microsecond=0)
    # Add a minute if the original seconds were 30 or more
    return rounded_dt + timedelta(minutes=1) if dt.second >= 30 else rounded_dt

class Assignment:
    def __init__(self, name, course, prof, due_date, due_time, pts, status, weight):
        self.name = name          #To the user, the Assignment's name is a better identifier of what it is and knowing what the Assignment is would help determine the advice for it
        self.course = course
        self.prof = prof          #Professor won't be important for the student, but it will help to determine professor-based advice
        self.due_date = due_date
        self.due_time = due_time
        self.status = status
        self.points = pts
        self.weight_score = weight
    
    #Assignment Accessors
    def GetName(self):
        return self.name
    def GetCourse(self):
        return self.course
    def GetProf(self):
        return self.prof
    def GetDate(self):
        return self.due_date
    def GetTime(self):
        return self.due_time
    def GetStatus(self):
        return self.status
    def GetPoints(self):
        return self.points
    def GetWeight(self):
        return self.weight_score

AssignmentList = {} #Will store all Assignments across pages, keyed by IDs
