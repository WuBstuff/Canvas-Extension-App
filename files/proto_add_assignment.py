#This is a prototype of the add assignment page
#When the user wants to add a new assignment, this page is opened up
import streamlit as sl
import datetime as dt
from assignment import *

#Helper Function
def generate_times():
    """Generates a list of times in 12-hour AM/PM format (e.g., '12:00 AM')."""
    times = []
    for h in range(24):
        for m in [0, 15, 30, 45]: # You can adjust the minute interval
            # Create a datetime object to use for formatting
            time_obj = dt.datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time()
            # Format to 12-hour with AM/PM using strftime
            times.append(time_obj.strftime("%I:%M %p"))
    return times
times = generate_times()

#Assignment Menu
sl.title("Add New Assignment")
sl.header("Add Assignment Menu")

sl.subheader("Name")
name = sl.text_input("Input Assignment Name")
sl.subheader("Professor")
prof = sl.text_input("Input Professor's Name")

col1, col2 = sl.columns(2)
with col1:
    sl.subheader("From")
    start_date = sl.date_input("Start Day")
with col2:
    sl.subheader("To")
    end_date = sl.date_input("End Day")

col1, col2 = sl.columns(2)
with col1:
    sl.subheader("From")
    start_time = sl.selectbox("Start Time", times)
with col2:
    sl.subheader("To")
    end_time = sl.selectbox("End Time", times)

sl.subheader("Status")
status = sl.selectbox("Assignment Status", ("Not Started", "Incomplete", "Halfway Done", "Almost Done"))

col1, col2 = sl.columns(2)
with col1:
    if sl.button("Back"):
        sl.switch_page("proto_dashboard.py")
with col2:
    if sl.button("Confirm"):
        new_assignment = Assignment(name, prof, start_date, end_date, start_time, end_time, status, "Advice goes here")
        AssignmentList.append(new_assignment)
        sl.switch_page("proto_dashboard.py")
