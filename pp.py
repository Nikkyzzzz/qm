import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ---- SETTINGS ----
STATE_FILE = "checklist_state.json"
TOTAL_TASKS = 101

# ---- FUNCTIONS ----
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def checklist(unit_name, start, end):
    st.markdown(f"### ✅ {unit_name}")
    for i in range(start, end + 1):
        key = f"task_{i}"
        current_val = checklist_state.get(key, False)
        updated_val = st.checkbox(f"Task {i}", value=current_val, key=key)
        checklist_state[key] = updated_val

# ---- LOAD STATE ----
checklist_state = load_state()

# ---- TITLE & TIME ----
st.title("📚 Exam Checklist with Save")
st.subheader("Persistent Tasks 1–101")

from datetime import datetime, timedelta

now = datetime.now()

# If it's already past 9:30 AM today, set it for tomorrow
exam_time = datetime.combine(
    now.date(), datetime.strptime("09:30", "%H:%M").time()
)
if now.time() > exam_time.time():
    exam_time += timedelta(days=1)

time_left = exam_time - now
hours_left = time_left.total_seconds() / 3600
st.info(f"⏰ Time left until exam: **{int(hours_left)} hours and {int((hours_left%1)*60)} minutes**")

# ---- UNIT TIME ALLOCATION ----
unit_names = ['Unit 1 (1–16)', 'Unit 2 (17–40)', 'Unit 3 (41–65)', 'Unit 4 (66–85)', 'Unit 5 (86–101)']
unit_ranges = [(1, 16), (17, 40), (41, 65), (66, 85), (86, 101)]
unit_lengths = [end - start + 1 for (start, end) in unit_ranges]
unit_times = [(l / TOTAL_TASKS) * hours_left for l in unit_lengths]

st.markdown("### 🕒 Suggested Time Allocation:")
for name, t in zip(unit_names, unit_times):
    st.write(f"- **{name}**: {int(t)} hr {int((t % 1) * 60)} min")

# ---- CHECKLIST SECTIONS ----
for name, (start, end) in zip(unit_names, unit_ranges):
    checklist(name, start, end)

# ---- SAVE BUTTON ----
if st.button("💾 Save Progress"):
    save_state(checklist_state)
    st.success("Checklist progress saved successfully!")

# ---- AUTO SAVE (optional) ----
save_state(checklist_state)