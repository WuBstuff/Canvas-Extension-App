#This file holds the Assignment class, which outlines how Assignments are stored and changed, subject to change
import datetime as dt
class Assignment:

    def __init__(self, name, prof, start_date, end_date, start_time, end_time, status, advice):
        self.name = name
        self.prof = prof
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.advice = advice

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
    def EditAdvice(self, new_advice):  #Note: Not used by the student, it will be generated/changed by the logic
        self.advice = new_advice
    def EditStatus(self, new_status):
        self.status = new_status
        if self.status == "Complete":  #No need for this assignment in the dashboard if it's done
            del self
    
    #Assignment Accessors
    def GetName(self):
        return self.name
    def GetProf(self):
        return self.prof
    def GetSDate(self):
        return self.start_date
    def GetEDate(self):
        return self.end_date
    def GetSTime(self):
        return self.start_time
    def GetETime(self):
        return self.end_time
    def GetAdvice(self):
        return self.advice
    def GetStatus(self):
        return self.status

    #This particular function will be useful for the logic needed for advice
    def GetTimeLeft(self):
        return dt.datetime.combine(self.end_date, self.end_time) - dt.datetime.now()
    
AssignmentList = []
