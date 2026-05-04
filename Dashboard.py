import streamlit as sl
from datetime import datetime, timedelta

from data.assignment import AssignmentList
from data.event import EventList


def _parse_datetime(value):
    if isinstance(value, datetime):
        return value
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    iso_text = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        return datetime.fromisoformat(iso_text)
    except ValueError:
        pass

    for date_format in ("%Y-%m-%d %I:%M %p", "%Y-%m-%d", "%m/%d/%Y %I:%M %p"):
        try:
            return datetime.strptime(text, date_format)
        except ValueError:
            continue

    return None


def _format_datetime(value):
    parsed = _parse_datetime(value)
    if parsed is None:
        return str(value) if value else "No date"
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone()
    return parsed.strftime("%b %d, %Y %I:%M %p").replace(" 0", " ")


def _format_time_left(value):
    parsed = _parse_datetime(value)
    if parsed is None:
        return "No due date"

    now = datetime.now(parsed.tzinfo) if parsed.tzinfo else datetime.now()
    remaining = parsed - now
    if remaining.total_seconds() <= 0:
        return "Past due"

    total_minutes = int(remaining.total_seconds() // 60)
    days, day_remainder = divmod(total_minutes, 24 * 60)
    hours, minutes = divmod(day_remainder, 60)

    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def _format_points(points):
    if points in (None, ""):
        return "0"
    try:
        number = float(points)
    except (TypeError, ValueError):
        return str(points)
    return str(int(number)) if number.is_integer() else f"{number:g}"


def _assignment_advice(due_at, points):
    parsed = _parse_datetime(due_at)
    if parsed is None:
        return "Add a deadline before scheduling."

    now = datetime.now(parsed.tzinfo) if parsed.tzinfo else datetime.now()
    remaining = parsed - now
    if remaining.total_seconds() <= 0:
        return "Review this overdue item."
    if remaining <= timedelta(days=1):
        return "Work on this first."
    if remaining <= timedelta(days=3):
        return "Schedule a focused block soon."

    try:
        if float(points or 0) >= 50:
            return "Reserve a longer study block."
    except (TypeError, ValueError):
        pass

    return "Plan time before the deadline."


def _canvas_assignment_rows(assignments):
    rows = []
    for assignment in assignments:
        title = assignment.get("title") or assignment.get("name") or "Untitled"
        due_at = assignment.get("due_at") or assignment.get("start_at")
        points = assignment.get("points")
        rows.append({
            "Assignment": title,
            "Class": assignment.get("context") or assignment.get("course") or "Unknown",
            "Due": _format_datetime(due_at),
            "Time Left": _format_time_left(due_at),
            "Points": _format_points(points),
            "Advice": _assignment_advice(due_at, points),
        })
    return rows


def _prototype_assignment_rows():
    rows = []
    for assignment in AssignmentList.values():
        due_at = f"{assignment.GetDate()} {assignment.GetTime()}"
        points = assignment.GetPoints()
        rows.append({
            "Assignment": assignment.GetName(),
            "Class": assignment.GetCourse(),
            "Due": _format_datetime(due_at),
            "Time Left": _format_time_left(due_at),
            "Points": _format_points(points),
            "Advice": _assignment_advice(due_at, points),
        })
    return rows


def _canvas_event_rows(events):
    rows = []
    for event in events:
        start = event.get("start") or event.get("start_at")
        end = event.get("end") or event.get("end_at")
        rows.append({
            "Event": event.get("title") or "Untitled",
            "Start": _format_datetime(start),
            "End": _format_datetime(end),
            "Calendar": event.get("context") or "Personal",
        })
    return rows


def _prototype_event_rows():
    rows = []
    for event in EventList.values():
        start = f"{event.GetDate()} {event.GetTime()}"
        rows.append({
            "Event": event.GetTitle(),
            "Start": _format_datetime(start),
            "End": "No end time",
            "Calendar": event.GetLoc(),
            "Frequency": event.GetFreq(),
        })
    return rows


def _render_workload(raw_data):
    assignments = raw_data.get("assignments", []) if raw_data else []
    events = raw_data.get("events", []) if raw_data else []

    if raw_data is None:
        assignment_rows = _prototype_assignment_rows()
        event_rows = _prototype_event_rows()
    else:
        assignment_rows = _canvas_assignment_rows(assignments)
        event_rows = _canvas_event_rows(events)

    sl.header("Assignment List")
    if assignment_rows:
        sl.dataframe(assignment_rows, use_container_width=True, hide_index=True)
    else:
        sl.info("No assignments found for the selected range.")

    sl.header("Event List")
    if event_rows:
        sl.dataframe(event_rows, use_container_width=True, hide_index=True)
    else:
        sl.info("No events found for the selected range.")


def _render_schedule(schedule):
    if not schedule:
        sl.info("Run the optimizer after fetching Canvas data to generate study blocks.")
        return

    rows = []
    for event in schedule:
        rows.append({
            "Study Block": event.get("title", "Study block"),
            "Start": _format_datetime(event.get("start_at")),
            "End": _format_datetime(event.get("end_at")),
            "Details": event.get("description", ""),
        })
    sl.dataframe(rows, use_container_width=True, hide_index=True)


def ViewDashboard(on_run_optimizer=None):
    raw_data = sl.session_state.get("raw_data")
    authenticated = sl.session_state.get("authenticated", False)

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
                sl.caption(f"{AssignmentList[index].GetDate()} by {AssignmentList[index].GetTime()} ({AssignmentList[index].GetTimeLeft()} left)")
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
                sl.caption(sl.caption(f"{EventList[index].GetDate()} by {EventList[index].GetTime()} ({EventList[index].GetTimeLeft()} left)"))
            with col3:
                sl.caption(EventList[index].GetFreq())
            with col4:
                sl.caption(EventList[index].GetLoc())
            with col5:
                sl.caption("Generated event advice goes here")
    
    #Tell the user to add something when there is nothing
    if len(AssignmentList) == 0 and len(EventList) == 0:
        sl.write("This planner is empty, perhaps reality has decided to give you free time.")
    elif len(AssignmentList) == 0:
        sl.write("There are no assignments to plan for. Now would be a good time to enjoy your events.")
    elif len(EventList) == 0:
        sl.write("There are no events to plan for. All that remains are your assignments and you are free.")
