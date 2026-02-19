import streamlit as st
import pandas as pd
from data.canvas_client import CanvasInterface
from logic.scheduler import SmartScheduler
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
            # API LEAD: This is where your code is called
            # ci = CanvasInterface(user_token)
            # st.session_state.raw_data = ci.get_everything()
            
            # MOCK DATA FOR SKELETON TESTING
            st.session_state.raw_data = {"user": "Test Student", "assignments": []}
            st.session_state.authenticated = True
            st.success("Connected!")
        else:
            st.error("Please enter a valid token.")

# --- 3. MAIN DASHBOARD LOGIC ---
if st.session_state.authenticated:
    st.write(f"Welcome back, **{st.session_state.raw_data['user']}**!")
    
    # Create Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Current Tasks", "Smart Schedule", "Settings"])
    
    with tab1:
        st.subheader("Your Canvas Assignments")
        # UI LEAD: Display data here
        if st.session_state.raw_data['assignments']:
            st.dataframe(st.session_state.raw_data['assignments'])
        else:
            st.info("No assignments found. Hit 'Refresh' to pull new data.")

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
