#This file holds the Event class, which outlines how Events are stored and changed, subject to change
import datetime as dt
class Event:

    def __init__(self, title, date, stime, etime, frequency, location, advice):
        self.title = title
        self.date = date
        self.start_time = stime
        self.end_time = etime
        self.frequency = frequency
        self.location = location
        self.advice = advice
    
    #Event Mutators
    def EditTitle(self, new_title):
        self.title = new_title
    def EditDate(self, new_date):
        self.date = new_date
    def EditSTime(self, new_stime):
        self.start_time = new_stime
    def EditETime(self, new_etime):
        self.end_time = new_etime
    def EditFreq(self, new_freq):
        self.frequency = new_freq
    def EditLoc(self, new_loc):
        self.location = new_loc
    def EditAdvice(self, new_advice):  #Note: same as with Assignment; advice will be managed by the program and not the student
        self.location = new_advice
    
    #This particular function will be useful for the logic needed for advice
    def GetTimeLeft(self):
        return dt.datetime.combine(self.date, self.end_time) - dt.datetime.now()
