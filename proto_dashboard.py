#This is a barebones prototype of how we want the Canvas dashboard to look like
#Some stuff to work on here would be the formatting of the dashboard as well as adding some extra things but this is just the basics
#In order to run this:
# type "python -m venv venv" into the terminal, this will create the venv folder needed to run the venv VM, don't need to do this if you already have a venv folder
# type "venv/bin/activate" into the terminal, this activates the Venv VM
# ensure that the debugger on VSCode or whatever IDE is set to the Venv version
# run the file with "streamlit run proto_dashboard.py", this opens up a window on your browser with the dashboard

import streamlit as sl

sl.set_page_config(
    page_title = "Canvas Dashboard",
    layout = "wide"
)
sl.title("Welcome to your Canvas Dashboard!")
sl.markdown("Here is the plan")

col1, col2, col3 = sl.columns(3)
with col1:
    sl.subheader("To-Do List:")
with col2:
    sl.button("Refresh Token")
with col3:
    sl.button("Input Token")

col1, col2, col3 = sl.columns(3)
with col1:
    sl.caption("Assignment 1")
with col2:
    sl.caption("Due by Tomorrow 11:59pm")
with col3:
    sl.caption("Get it done ASAP, today afterschool would be good")

col1, col2, col3 = sl.columns(3)
with col1:
    sl.caption("Assignment 2")
with col2:
    sl.caption("Due in 3 days 8am")
with col3:
    sl.caption("You got some time, maybe put it off to work on Assignment 1")

col1, col2, col3 = sl.columns(3)
with col1:
    sl.caption("Quiz 1")
with col2:
    sl.caption("Starts next Monday from 8am to 10am")
with col3:
    sl.caption("Shouldn't be too bad; an hour or two of studying should be fine")

col1, col2 = sl.columns(2)
with col1:
    sl.button("Add Assignment")
with col2:
    sl.button("Edit Assignment")
