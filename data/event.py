#This file holds the Event class, which outlines how Events are stored and changed, subject to change

from datetime import datetime, timedelta

def round_to_nearest_minute(dt):
    # Round down to the nearest minute by stripping seconds/microseconds
    rounded_dt = dt.replace(second=0, microsecond=0)
    # Add a minute if the original seconds were 30 or more
    return rounded_dt + timedelta(minutes=1) if dt.second >= 30 else rounded_dt

class Event:

    def __init__(self, title, date, time, frequency, location):
        self.title = title
        self.date = date
        self.time = time
        self.frequency = frequency
        self.location = location
    
    #Event Mutators
    def EditTitle(self, new_title):
        self.title = new_title
    def EditDate(self, new_date):
        self.date = new_date
    def EditTime(self, new_time):
        self.time = new_time
    def EditFreq(self, new_freq):
        self.frequency = new_freq
    def EditLoc(self, new_loc):
        self.location = new_loc

    #Event Accessors
    def GetTitle(self):
        return self.title
    def GetDate(self):
        return self.date
    def GetTime(self):
        return self.time
    def GetFreq(self):
        return self.frequency
    def GetLoc(self):
        return self.location
    def GetTimeLeft(self):
        dt_str = f"{self.date[:4]}-{self.date[5:7]}-{self.date[8:]} {self.time}"
        dt_format = "%Y-%m-%d %I:%M %p"
        due = round_to_nearest_minute(datetime.strptime(dt_str, dt_format)) - round_to_nearest_minute(datetime.now())
        return due
    
EventList = {} #Store all events across pages with IDs are their keys
