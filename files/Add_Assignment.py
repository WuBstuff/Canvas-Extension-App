#This is a prototype of the add assignment page
#When the user wants to add a new assignment, this page is opened up
import streamlit as sl
from datetime import datetime, timedelta
from assignment import *

#Helper Functions
def round_to_nearest_minute(dt):
    # Round down to the nearest minute by stripping seconds/microseconds
    rounded_dt = dt.replace(second=0, microsecond=0)
    # Add a minute if the original seconds were 30 or more
    return rounded_dt + timedelta(minutes=1) if dt.second >= 30 else rounded_dt

def generate_times():
    """Generates a list of times in 12-hour AM/PM format (e.g., '12:00 AM')."""
    times = []
    for h in range(24):
        for m in [0, 15, 30, 45]: # You can adjust the minute interval
            # Create a datetime object to use for formatting
            time_obj = datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time()
            # Format to 12-hour with AM/PM using strftime
            times.append(time_obj.strftime("%I:%M %p"))
    return times

times = generate_times()

#Assignment Menu
sl.title("Add New Assignment")
sl.header("Add Assignment Menu")

sl.subheader("Name")
name = sl.text_input("Input Assignment Name")
sl.subheader("Course")
course = sl.text_input("Input Course Name")
sl.subheader("Professor")
prof = sl.text_input("Input Professor's Name")

sl.subheader("Due Date")
end_date = str(sl.date_input("End Day"))
sl.subheader("Due Time")
end_time = str(sl.selectbox("End Time", times))
dt_str = f"{end_date[:4]}-{end_date[5:7]}-{end_date[8:]} {end_time}"
dt_format = "%Y-%m-%d %I:%M %p"
due = round_to_nearest_minute(datetime.strptime(dt_str, dt_format)) - round_to_nearest_minute(datetime.now())

sl.subheader("Points")
points = sl.number_input("Input Points")
sl.subheader("Weight Percent")
weight_percent = sl.text_input("Input Grade Weight")
sl.subheader("Status")
status = sl.selectbox("Assignment Status", ("Unsubmitted", "Submitted", "Graded"))

col1, col2 = sl.columns(2)
with col1:
    if sl.button("Back"):
        sl.switch_page("Dashboard.py")
with col2:
    if sl.button("Confirm"):
        id = len(AssignmentList) + 1
        new_assignment = Assignment(id, name, course, prof, due, points, status, weight_percent)
        AssignmentList.append(new_assignment)
        AssignmentList.sort(key= lambda assignment: getattr(assignment, 'due_date')) #sort the assignment list with earliest due dates first
        sl.switch_page("Dashboard.py")
