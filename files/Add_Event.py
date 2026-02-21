#This is a prototype of the add event page
#When the user wants to add a new event, this page is opened up

import streamlit as sl
from datetime import datetime, timedelta
from event import *

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
            time_obj = dt.datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time()
            # Format to 12-hour with AM/PM using strftime
            times.append(time_obj.strftime("%I:%M %p"))
    return times
times = generate_times()

#Event Menu
sl.title("Add New Event")
sl.header("Add Event Menu")

sl.subheader("Title")
title = sl.text_input("Input Event Title")

sl.subheader("Date")
date = str(sl.date_input("Input Date"))
sl.subheader("Time")
time = str(sl.selectbox("Input Time", times))
dt_str = f"{date[:4]}-{date[5:7]}-{date[8:]} {time}"
dt_format = "%Y-%m-%d %I:%M %p"
time_left = round_to_nearest_minute(datetime.strptime(dt_str, dt_format)) - round_to_nearest_minute(datetime.now())

sl.subheader("Frequency")
frequency = sl.selectbox("Select your event's frequency:", ("Does not repeat", "Daily", "Weekly", "Monthly", "Annually", "Every weekday", "Custom"))
sl.subheader("Location")
location = sl.text_input("Input Event Location")

col1, col2 = sl.columns(2)
with col1:
    if sl.button("Back"):
        sl.switch_page("Dashboard.py")
with col2:
    if sl.button("Confirm"):
        id = len(EventList) + 1
        new_event = Event(id, title, time_left, frequency, location)
        EventList.append(new_event)
        sl.switch_page("Dashboard.py")
