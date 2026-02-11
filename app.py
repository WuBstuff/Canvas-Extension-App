import streamlit as st
from data.canvas_client import CanvasInterface
from logic.scheduler import SmartScheduler

# 1. Sidebar - Token Input
token = st.sidebar.text_input("Canvas Token", type="password")

if token:
    # 2. Fetch Data
    ci = CanvasInterface(token, "https://canvas.instructure.com")
    
    # 3. Show Analytics (Grades, Professor info)
    st.header("Your Academic Snapshot")
    
    # 4. The "Sync" Button
    if st.button("Generate Smart Schedule"):
        # Run the logic and display the preview
        # Then offer a button to "Commit to Canvas"
