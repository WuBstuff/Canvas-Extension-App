import streamlit as st
import pandas as pd
from data.canvas_client import CanvasInterface
from logic.scheduler import SmartScheduler
from datetime import datetime, timedelta
# Import your teammates' work (once files are created)
# from data.canvas_client import CanvasInterface
# from logic.scheduler import SmartScheduler

# --- 1. SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'processed_schedule' not in st.session_state:
    st.session_state.processed_schedule = None

st.title("Smart Canvas Planner")

# --- 2. SIDEBAR: AUTHENTICATION ---
with st.sidebar:
    st.header("Authentication")
    user_token = st.text_input("Enter Canvas Manual Token", type="password")
    
    if st.button("Connect to Canvas"):
        if user_token:
            # Initialize Interface
            ci = CanvasInterface(user_token, "https://csufullerton.instructure.com")
            # Store the interface and the list of sources in session state
            st.session_state.ci = ci
            st.session_state.calendar_options = ci.get_calendar_sources()
            st.session_state.authenticated = True
            st.success("Connected! Now select your calendars.")

    # Only show the selection and fetch button IF authenticated
    if st.session_state.authenticated:
        st.divider()
        st.header("Calendar Selection")
        
        # Create a display-friendly list for the multiselect
        options = st.session_state.calendar_options
        selected_names = st.multiselect(
            "Select Calendars to Sync",
            options=[opt["name"] for opt in options],
            default=[opt["name"] for opt in options] # Default to all selected
        )
        
        # Map the selected names back to their IDs
        selected_ids = [opt["id"] for opt in options if opt["name"] in selected_names]

        if st.button("Fetch Assignments"):
            with st.spinner("Fetching data..."):
                # Use your existing date logic (e.g., next 14 days)
                start = datetime.now().strftime("%Y-%m-%d")
                end = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                
                # Fetch data using only the selected IDs
                workload = st.session_state.ci.get_student_workload(start, end, calendar_ids=selected_ids)
                
                # Update raw_data for the dashboard
                st.session_state.raw_data = {
                    "user": st.session_state.ci.user.name,
                    "assignments": workload
                }
                st.success(f"Pulled {len(workload)} assignments!")

# --- 3. MAIN DASHBOARD LOGIC ---
if st.session_state.authenticated:
    
    # Create Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Current Tasks", "Smart Schedule", "Settings"])
    
    with tab1:
        st.subheader("Your Canvas Assignments")
        # UI LEAD: Display data here
        if st.session_state.raw_data is not None:
            if st.session_state.raw_data['assignments']:
                st.dataframe(st.session_state.raw_data['assignments'])
            else:
                st.info("No assignments found for the selected range.")
        else:
            # Tell the user what to do next
            st.warning("👈 Please select your calendars and click 'Fetch Assignments' in the sidebar.")
            

    with tab2:
        st.subheader("AI Predicted Work Blocks")
        if st.button("Run Optimizer"):
            # LOGIC LEAD: This is where your scheduler is called
            # scheduler = SmartScheduler(st.session_state.raw_data)
            # st.session_state.processed_schedule = scheduler.generate()
            st.write("Optimization logic running...")
            
    with tab3:
        if st.button("Clear Session"):
            st.session_state.clear()
            st.rerun()

else:
    st.info("Please enter your Canvas Token in the sidebar to begin.")




# # 1. Sidebar - Token Input
# token = st.sidebar.text_input("Canvas Token", type="password")

# if token:
#     # 2. Fetch Data
#     ci = CanvasInterface(token, "https://canvas.instructure.com")
    
#     # 3. Show Analytics (Grades, Professor info)
#     st.header("Your Academic Snapshot")
    
#     # 4. The "Sync" Button
#     if st.button("Generate Smart Schedule"):
#         # Run the logic and display the preview
#         # Then offer a button to "Commit to Canvas"
