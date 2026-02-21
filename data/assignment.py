#This file holds the Assignment class, which outlines how Assignments are stored and changed, subject to change
import datetime as dt
class Assignment:

    def __init__(self, id, name, course, prof, due_date, pts, status, weight):
        self.id = id              #ID won't be changed, it differentiates Assignments from each other
        self.name = name          #To the user, the Assignment's name is a better identifier of what it is and knowing what the Assignment is would help determine the advice for it
        self.course = course
        self.prof = prof          #Professor won't be important for the student, but it will help to determine professor-based advice
        self.due_date = due_date
        self.status = status
        self.points = pts
        self.weight_score = weight

    #Assignment Mutators
    def EditName(self, new_name):
        self.name = new_name
    def EditCourse(self, new_course):
        self.course = new_course
    def EditProf(self, new_prof):
        self.prof = new_prof
    def EditDue(self, new_date):
        self.due_date = new_date
    def EditStatus(self, new_status):
        self.status = new_status
    def EditPoints(self, new_pts):
        self.points = new_pts
    def EditWeight(self, new_weight):
        self.weight_score = new_weight
    
    #Assignment Accessors
    def GetName(self):
        return self.name
    def GetCourse(self):
        return self.course
    def GetProf(self):
        return self.prof
    def GetDue(self):
        return self.due_date
    def GetStatus(self):
        return self.status
    def GetPoints(self):
        return self.points
    def GetWeight(self):
        return self.weight_score
    
AssignmentList = [] #Will store all Assignments across pages
