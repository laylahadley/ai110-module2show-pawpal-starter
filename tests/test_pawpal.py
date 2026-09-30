from datetime import date, datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task

DAY = datetime(2026, 1, 1)


def at(hour: int, minute: int = 0) -> datetime:
    """Build a datetime on the fixed test day."""
    return DAY.replace(hour=hour, minute=minute)


def make_task(
    description: str = "Walk",
    time: datetime = None,
    duration: int = 15,
    frequency: str = "once",
) -> Task:
    """Build a task with sensible defaults for tests."""
    return Task(
        description=description,
        category="general",
        time=time or at(8),
        duration_minutes=duration,
        frequency=frequency,
    )


def make_scheduler():
    """Build an owner with two pets (no tasks) and a scheduler for them."""
    owner = Owner(name="Jordan")
    buddy = Pet(name="Buddy", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(buddy)
    owner.add_pet(mochi)
    return Scheduler(owner), buddy, mochi


# ---- Basics (per phase 2) ----

def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1


# ---- sorting ----

def test_sort_by_time_returns_chronological_order():
    scheduler, buddy, mochi = make_scheduler()
    buddy.add_task(make_task("Dinner", at(18)))
    mochi.add_task(make_task("Breakfast", at(7)))
    buddy.add_task(make_task("Lunch", at(12)))
    result = scheduler.sort_by_time()
    assert [t.description for t in result] == ["Breakfast", "Lunch", "Dinner"]


def test_sort_with_no_tasks_returns_empty_list():
    scheduler, _, _ = make_scheduler()
    assert scheduler.sort_by_time() == []


# ---- filtering ----

def test_filter_by_pet_name_returns_only_that_pets_tasks():
    scheduler, buddy, mochi = make_scheduler()
    buddy.add_task(make_task("Walk", at(8)))
    mochi.add_task(make_task("Medicine", at(9)))
    result = scheduler.filter_tasks(pet_name="Buddy")
    assert [t.description for t in result] == ["Walk"]


def test_filter_by_completion_status():
    scheduler, buddy, _ = make_scheduler()
    done = make_task("Done task", at(8))
    pending = make_task("Pending task", at(9))
    buddy.add_task(done)
    buddy.add_task(pending)
    scheduler.mark_task_complete(done)  # frequency is "once", so no new task
    assert scheduler.filter_tasks(completed=True) == [done]
    assert scheduler.filter_tasks(completed=False) == [pending]



# ---- recurrence ----

def test_daily_task_completion_creates_next_day_task():
    scheduler, buddy, _ = make_scheduler()
    task = make_task("Walk", at(8), frequency="daily")
    buddy.add_task(task)
    next_task = scheduler.mark_task_complete(task)
    assert task.completed is True
    assert next_task is not None
    assert next_task.time == at(8) + timedelta(days=1)
    assert next_task.completed is False
    assert len(buddy.tasks) == 2


def test_weekly_task_completion_creates_task_one_week_later():
    scheduler, buddy, _ = make_scheduler()
    task = make_task("Bath", at(10), frequency="weekly")
    buddy.add_task(task)
    next_task = scheduler.mark_task_complete(task)
    assert next_task.time == at(10) + timedelta(days=7)
    assert len(buddy.tasks) == 2


def test_one_time_task_completion_does_not_create_new_task():
    scheduler, buddy, _ = make_scheduler()
    task = make_task("Vet visit", at(14), frequency="once")
    buddy.add_task(task)
    assert scheduler.mark_task_complete(task) is None
    assert len(buddy.tasks) == 1



# ---- conflict detection ----

def test_same_start_time_is_flagged_as_conflict():
    scheduler, buddy, mochi = make_scheduler()
    buddy.add_task(make_task("Feed Buddy", at(8)))
    mochi.add_task(make_task("Give Mochi medicine", at(8)))
    assert len(scheduler.find_conflicts()) == 1
    warnings = scheduler.get_conflict_warnings()
    assert len(warnings) == 1
    assert "Feed Buddy" in warnings[0] and "Give Mochi medicine" in warnings[0]


def test_overlapping_durations_are_flagged_as_conflict():
    scheduler, buddy, _ = make_scheduler()
    buddy.add_task(make_task("Walk", at(8), duration=30))
    buddy.add_task(make_task("Feed", at(8, 15)))
    assert len(scheduler.find_conflicts()) == 1


def test_back_to_back_tasks_are_not_conflicts():
    scheduler, buddy, _ = make_scheduler()
    buddy.add_task(make_task("Walk", at(8), duration=30))
    buddy.add_task(make_task("Feed", at(8, 30)))
    assert scheduler.find_conflicts() == []


def test_completed_tasks_are_ignored_by_conflict_detection():
    scheduler, buddy, mochi = make_scheduler()
    first = make_task("Feed Buddy", at(8))
    buddy.add_task(first)
    mochi.add_task(make_task("Give Mochi medicine", at(8)))
    scheduler.mark_task_complete(first)
    assert scheduler.find_conflicts() == []


# ---- edge cases ----

def test_pets_with_no_tasks_cause_no_errors():
    scheduler, _, _ = make_scheduler()
    assert scheduler.owner.get_all_tasks() == []
    assert scheduler.get_todays_tasks() == []
    assert scheduler.find_conflicts() == []
    assert scheduler.get_conflict_warnings() == []


def test_todays_tasks_excludes_other_days():
    scheduler, buddy, _ = make_scheduler()
    buddy.add_task(make_task("Today walk", at(8)))
    buddy.add_task(make_task("Tomorrow walk", at(8) + timedelta(days=1)))
    result = scheduler.get_todays_tasks(today=date(2026, 1, 1))
    assert [t.description for t in result] == ["Today walk"]