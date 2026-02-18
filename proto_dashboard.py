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
col1, col2, col3 = sl.columns(3)
with col1:
    sl.subheader("Here is the plan:")
with col2:
    sl.button("Refresh Token")
with col3:
    sl.button("Input Token")

sl.header("Assignment List")
for index in range(len(AssignmentList)):
    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.caption(AssignmentList[index].GetName())
    with col2:
        sl.caption(AssignmentList[index].GetEDate())
    with col3:
        sl.caption(AssignmentList[index].GetAdvice())

#Event Display
sl.header("Event List")
for index in range(len(EventList)):
    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.caption(EventList[index].GetTitle())
    with col2:
        sl.caption(EventList[index].GetSTime())
    with col3:
        sl.caption(EventList[index].GetAdvice())
