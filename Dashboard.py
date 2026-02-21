#This is a barebones prototype of how we want the Canvas dashboard to look like through StreamLit
#Some stuff to work on here would be the formatting of the dashboard as well as adding some extra things but this is just the basics
#In order to run this:
# type "python -m venv venv" into the terminal, this will create the venv folder needed to run the venv VM
# type "venv/bin/activate" into the terminal, this activates the Venv VM
# ensure that the debugger on VSCode or whatever IDE is set to the Venv version
# run the file with "streamlit run proto_dashboard.py", this opens up a window on your browser with the dashboard

import streamlit as sl
from event import *
from assignment import *

#Page Settings
sl.set_page_config(
    page_title = "My Canvas Dashboard",
    layout = "wide"
)
sl.title("Welcome to your Canvas Dashboard!")

#Workload Display
if len(AssignmentList) > 0:
    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.subheader("Here is the plan:")
    with col2:
        sl.button("Refresh Token")
    with col3:
        sl.button("Input Token")
    sl.header("Assignment List")
    col1, col2, col3, col4, col5 = sl.columns(5)
    with col1:
        sl.write("Assignment")
    with col2:
        sl.write("Class")
    with col3:
        sl.write("Time Left")
    with col4:
        sl.write("Point Worth")
    with col5:
        sl.write("Advice")
    for index in range(len(AssignmentList)):
        col1, col2, col3, col4, col5 = sl.columns(5)
        with col1:
            sl.caption(AssignmentList[index].GetName())
        with col2:
            sl.caption(AssignmentList[index].GetCourse())
        with col3:
            sl.caption(AssignmentList[index].GetDue())
        with col4:
            sl.caption(AssignmentList[index].GetPoints())
        with col5:
            sl.caption("Generated assignment advice goes here")

#Event Display
if len(EventList) > 0:
    sl.header("Event List")
    col1, col2, col3, col4, col5 = sl.columns(5)
    with col1:
        sl.write("Event")
    with col2:
        sl.write("Time")
    with col3:
        sl.write("Location")
    with col4:
        sl.write("Frequency")
    with col5:
        sl.write("Advice")
    for index in range(len(EventList)):
        col1, col2, col3, col4, col5 = sl.columns(5)
        with col1:
            sl.caption(EventList[index].GetTitle())
        with col2:
            sl.caption(EventList[index].GetTime())
        with col3:
            sl.caption(EventList[index].GetLoc())
        with col4:
            sl.caption(EventList[index].GetFreq())
        with col5:
            sl.caption("Generated event advice goes here")

#Tell the user to add something when there is nothing
if len(AssignmentList) == 0 and len(EventList) == 0:
    sl.write("This planner is empty, perhaps reality has decided to give you free time.")
elif len(AssignmentList) == 0:
    sl.write("There are no assignments to plan for. Now would be a good time to enjoy your events.")
elif len(EventList) == 0:
    sl.write("There are no events to plan for. All that remains are your assignments and you are free.")
