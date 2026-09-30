from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from typing import Optional



@dataclass
class Task:
    description: str
    category: str  # feeding, walk, medication, appointment
    time: datetime  # full date + time the task starts
    duration_minutes: int = 15  # used for overlap detection
    priority: str = "medium"  # low, medium, high
    frequency: str = "once"  # once, daily, weekly
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task belonging to the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def pet_name_for(self, task: Task) -> str:
        """Return the name of the pet that owns `task` ('?' if none does)."""
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                return pet.name
        return "?"

    def get_todays_tasks(self, today: Optional[date] = None) -> list[Task]:
        """Return the owner's tasks dated `today` (default: current date), sorted by time."""
        today = today or date.today()
        todays = [t for t in self.owner.get_all_tasks() if t.time.date() == today]
        return self.sort_by_time(todays)

    def sort_by_time(self, tasks: Optional[list[Task]] = None) -> list[Task]:
        """Sort tasks by start time; uses all of the owner's tasks if none are given."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> list[Task]:
        """Return tasks filtered by pet name and/or completion status, sorted by time."""
        pets = [p for p in self.owner.pets if pet_name is None or p.name == pet_name]
        tasks = [
            t
            for p in pets
            for t in p.tasks
            if completed is None or t.completed == completed
        ]
        return self.sort_by_time(tasks)

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task done; for daily/weekly tasks, add and return the next occurrence."""
        task.mark_complete()
        step = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(
            task.frequency
        )
        if step is None:
            return None
        next_task = replace(task, time=task.time + step, completed=False)
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                pet.add_task(next_task)
                break
        return next_task

    def find_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of unfinished tasks whose time windows overlap."""
        tasks = [t for t in self.sort_by_time() if not t.completed]
        conflicts = []
        for i, first in enumerate(tasks):
            first_end = first.time + timedelta(minutes=first.duration_minutes)
            for second in tasks[i + 1:]:
                if second.time >= first_end:
                    break  # sorted by start time, so no later task can overlap
                conflicts.append((first, second))
        return conflicts

    def get_conflict_warnings(self) -> list[str]:
        """Return a readable warning for each overlap instead of raising an error."""
        return [
            f"Conflict: {a.description} ({self.pet_name_for(a)}, {a.time:%I:%M %p}) "
            f"overlaps {b.description} ({self.pet_name_for(b)}, {b.time:%I:%M %p})"
            for a, b in self.find_conflicts()
        ]