from datetime import date, datetime 

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Keep one Owner alive across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )


st.divider()

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    clean_name = pet_name.strip()
    if not clean_name:
        st.warning("Enter a pet name first.")
    elif any(p.name == clean_name for p in owner.pets):
        st.warning(f"{clean_name} is already on your list.")
    else:
        owner.add_pet(Pet(name=clean_name, species=species))
        st.success(f"Added {clean_name}!")

if owner.pets:
    st.write("Your pets:")
    st.table([{"Name": p.name, "Species": p.species} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. Each task is saved on the pet you pick and feeds into the scheduler.")

if owner.pets:
    pet_choice = st.selectbox("Add task for", [p.name for p in owner.pets])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.time_input("Time")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == pet_choice)
        pet.add_task(
            Task(
                description=task_title,
                category="general",
                time=datetime.combine(date.today(), task_time),
                duration_minutes=int(duration),
                priority=priority,
            )
        )
        st.success(f"Added '{task_title}' for {pet.name}.")
else:
    st.info("Add a pet first, then you can add tasks.")

# Task has no pet field, so build a lookup for display
pet_of = {id(task): pet.name for pet in owner.pets for task in pet.tasks}
all_tasks = Scheduler(owner).sort_by_time()

if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Pet": pet_of[id(t)],
                "Task": t.description,
                "Time": t.time.strftime("%I:%M %p"),
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority,
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Builds today's schedule from your pets' tasks, sorted by time, and flags overlaps.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    todays = scheduler.get_todays_tasks()
    if todays:
        st.success(f"Today's schedule for {owner.name}:")
        st.table(
            [
                {
                    "Time": t.time.strftime("%I:%M %p"),
                    "Task": t.description,
                    "Pet": pet_of[id(t)],
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority,
                }
                for t in todays
            ]
        )
    else:
        st.info("No tasks scheduled for today. Add some above.")

    for first, second in scheduler.find_conflicts():
        st.warning(
            f"Conflict: {first.description} ({pet_of[id(first)]}) overlaps "
            f"{second.description} ({pet_of[id(second)]})"
        )
        