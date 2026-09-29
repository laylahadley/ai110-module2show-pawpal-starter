from datetime import datetime
from pawpal_system import Pet, Task


def make_task() -> Task:
    return Task(
        description="Morning walk",
        category="walk",
        time=datetime(2026, 1, 1, 8, 0),
    )


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

    