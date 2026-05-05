import streamlit as st
from data.canvas_client import CanvasInterface
from logic.scheduler import SmartScheduler
from datetime import datetime, timedelta
from Dashboard import ViewDashboard

CANVAS_BASE_URL = "https://csufullerton.instructure.com"

st.set_page_config(page_title="Smart Canvas Planner", layout="wide")


def _parse_canvas_datetime(value):
    if isinstance(value, datetime):
        return value
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _scheduler_datetime(value):
    parsed = _parse_canvas_datetime(value)
    if parsed is None:
        return None
    if parsed.tzinfo is not None:
        return parsed.astimezone().replace(tzinfo=None)
    return parsed


def _number_or_default(value, default=1):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _weight_or_default(value, default=1):
    if value in (None, ""):
        return default

    text = str(value).strip()
    if text.endswith("%"):
        text = text[:-1]

    try:
        weight = float(text)
    except (TypeError, ValueError):
        return default

    if weight > 1:
        return weight / 100
    return weight


def _build_scheduler_inputs(raw_data):
    assignments = []
    for assignment in raw_data.get("assignments", []):
        if not assignment.get("include", True):
            continue

        due_at = _scheduler_datetime(assignment.get("due_at") or assignment.get("start_at"))
        if due_at is None:
            continue

        course_name = (
            assignment.get("course_name")
            or assignment.get("context")
            or assignment.get("course")
            or "Unknown"
        )

        assignments.append({
            "name": assignment.get("title") or assignment.get("name") or "Untitled",
            "course_name": course_name,
            "due_at": due_at,
            "points": _number_or_default(assignment.get("points"), default=1),
            "group_weight": _weight_or_default(assignment.get("group_weight"), default=1),
            "assignment_group_name": assignment.get("assignment_group_name", "Unweighted"),
            "canvas_assignment_id": assignment.get("canvas_assignment_id"),
            "calendar_id": raw_data.get("personal_calendar_id"),
        })

    existing_events = []
    for event in raw_data.get("events", []):
        if not event.get("include", True):
            continue

        start = _scheduler_datetime(event.get("start") or event.get("start_at"))
        end = _scheduler_datetime(event.get("end") or event.get("end_at"))
        if start is not None and end is not None and end > start:
            existing_events.append((start, end))

    return assignments, existing_events


def run_optimizer():
    raw_data = st.session_state.get("raw_data")
    if not raw_data:
        st.warning("Fetch Canvas data before running the optimizer.")
        return

    assignments, existing_events = _build_scheduler_inputs(raw_data)
    if not assignments:
        st.session_state.processed_schedule = []
        st.warning("No assignments with due dates were available to schedule.")
        return

    try:
        scheduler = SmartScheduler(assignments, existing_events)
        st.session_state.processed_schedule = scheduler.generate_predictions()
    except Exception as exc:
        st.error(f"Could not generate the smart schedule: {exc}")
        return

    count = len(st.session_state.processed_schedule)
    if count:
        st.success(f"Generated {count} study block{'s' if count != 1 else ''}.")
    else:
        st.info("No open study blocks were found in the current schedule window.")

# --- 1. SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'processed_schedule' not in st.session_state:
    st.session_state.processed_schedule = None
if 'calendar_options' not in st.session_state:
    st.session_state.calendar_options = []
if 'raw_data_version' not in st.session_state:
    st.session_state.raw_data_version = 0

# --- 2. SIDEBAR: AUTHENTICATION ---
with st.sidebar:
    st.header("Authentication")
    user_token = st.text_input("Enter Canvas Manual Token", type="password")
    
    if st.button("Connect to Canvas"):
        if user_token:
            try:
                ci = CanvasInterface(user_token, CANVAS_BASE_URL)
                st.session_state.ci = ci
                st.session_state.calendar_options = ci.get_calendar_sources()
                st.session_state.authenticated = True
                st.session_state.raw_data = None
                st.session_state.processed_schedule = None
                st.success("Connected! Now select your calendars.")
            except Exception as exc:
                st.session_state.authenticated = False
                st.error(f"Could not connect to Canvas: {exc}")
        else:
            st.warning("Enter a Canvas token before connecting.")

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

        if st.button("Fetch Canvas Data"):
            with st.spinner("Fetching data..."):
                start = datetime.now().strftime("%Y-%m-%d")
                end = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                
                workload = st.session_state.ci.get_student_workload(start, end, calendar_ids=selected_ids)
                events = st.session_state.ci.get_existing_events(start, end, calendar_ids=selected_ids)
                
                st.session_state.raw_data = {
                    "user": st.session_state.ci.user.name,
                    "personal_calendar_id": f"user_{st.session_state.ci.user.id}",
                    "assignments": workload,
                    "events": events,
                }
                st.session_state.processed_schedule = None
                st.session_state.raw_data_version += 1
                st.success(f"Pulled {len(workload)} assignments and {len(events)} events!")

# --- 3. MAIN DASHBOARD LOGIC ---
ViewDashboard(on_run_optimizer=run_optimizer)
