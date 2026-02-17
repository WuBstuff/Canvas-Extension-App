#This file holds the Assignment class, which outlines how Assignments are stored and changed, subject to change
import datetime as dt
class Assignment:

    def __init__(self, prof, name, start_date, end_date, start_time, end_time, status, advice):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.advice = advice
        self.prof = prof

    #Assignment Mutators
    def EditName(self, new_name):
        self.name = new_name
    def EditProf(self, new_prof):
        self.prof = new_prof
    def EditSDate(self, new_sdate):
        self.start_date = new_sdate
    def EditEDate(self, new_edate):
        self.end_date = new_edate
    def EditSTime(self, new_stime):
        self.start_time = new_stime
    def EditETime(self, new_etime):
        self.end_time = new_etime
    def EditAdvice(self, new_advice):
        self.advice = new_advice
    def EditStatus(self, new_status):
        self.status = new_status
        if self.status == "Complete":  #No need for this assignment in the dashboard if it's done
            del self
    
    #Assignment Accessors (there might be more functions in the future idk)

    #This particular function will be useful for the logic needed for advice
    def GetTimeLeft(self):
        return dt.datetime.combine(self.end_date, self.end_time) - dt.datetime.now()
