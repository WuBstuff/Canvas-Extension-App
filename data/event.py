#This file holds the Event class, which outlines how Events are stored and changed, subject to change
class Event:

    def __init__(self, id, title, time_left, frequency, location):
        self.id = id
        self.title = title
        self.time = time_left
        self.frequency = frequency
        self.location = location
    
    #Event Mutators
    def EditTitle(self, new_title):
        self.title = new_title
    def EditTime(self, new_time):
        self.time = new_time
    def EditFreq(self, new_freq):
        self.frequency = new_freq
    def EditLoc(self, new_loc):
        self.location = new_loc

    #Event Accessors
    def GetTitle(self):
        return self.title
    def GetTime(self):
        return self.time
    def GetFreq(self):
        return self.frequency
    def GetLoc(self):
        return self.location
    
EventList = [] #Store all events across pages
