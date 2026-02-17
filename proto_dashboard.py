#This is a barebones prototype of how we want the Canvas dashboard to look like through StreamLit
#Some stuff to work on here would be the formatting of the dashboard as well as adding some extra things but this is just the basics
#In order to run this:
# type "python -m venv venv" into the terminal, this will create the venv folder needed to run the venv VM
# type "source venv/bin/activate" into the terminal, this activates the Venv VM
# ensure that the debugger on VSCode or whatever IDE is set to the Venv version
# run the file with "streamlit run proto_dashboard.py", this opens up a window on your browser with the dashboard

import streamlit as sl
import assignment #implement later, currently working on events

#Page Settings
sl.set_page_config(
    page_title = "My Canvas Dashboard",
    layout = "wide"
)
sl.title("Welcome to your Canvas Dashboard!")

#Sample Values
assignments = ("Assignment 1", "Assignment 2", "Quiz 1")
due_dates = ("Tomorrow 11:59pm", "Thursday 8am", "Next Monday from 8am to 10am")
advices = ("Get it done ASAP, today afterschool would be good", "You got some time, maybe put it off to work on Assignment 1", "Shouldn't be too bad; an hour or two of studying should be fine")

#Workload Display
col1, col2, col3 = sl.columns(3)
with col1:
    sl.subheader("Here is the (sample) plan:")
with col2:
    sl.button("Refresh Token")
with col3:
    sl.button("Input Token")

for index in range(len(assignments)):
    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.caption(assignments[index])
    with col2:
        sl.caption(due_dates[index])
    with col3:
        sl.caption(advices[index])
