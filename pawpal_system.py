from dataclasses import dataclass, field
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
        """Create a scheduler for an owner."""
        self.owner = owner

    def get_todays_tasks(self, today: Optional[date] = None) -> list[Task]:
        """Tasks from the owner's pets that fall on `today` (defaults to the current date)."""
        selected_date = today if today is not None else date.today()
        tasks = [task for task in self.owner.get_all_tasks() if task.time.date() == selected_date]
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: Optional[list[Task]] = None) -> list[Task]:
        """Sort by time. If no list is given, use all of the owner's tasks."""
        tasks_to_sort = tasks if tasks is not None else self.owner.get_all_tasks()
        return sorted(tasks_to_sort, key=lambda task: task.time)

    def find_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of the owner's tasks whose time windows overlap."""
        tasks = self.sort_by_time()
        conflicts: list[tuple[Task, Task]] = []

        for index, first_task in enumerate(tasks):
            first_end = first_task.time + timedelta(minutes=first_task.duration_minutes)
            for second_task in tasks[index + 1 :]:
                if second_task.time >= first_end:
                    break
                second_end = second_task.time + timedelta(minutes=second_task.duration_minutes)
                if first_task.time < second_end:
                    conflicts.append((first_task, second_task))

        return conflicts

    