from dataclasses import dataclass, field
from datetime import date, datetime
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
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_tasks(self, today: Optional[date] = None) -> list[Task]:
        """Tasks from the owner's pets that fall on `today` (defaults to the current date)."""
        pass

    def sort_by_time(self, tasks: Optional[list[Task]] = None) -> list[Task]:
        """Sort by time. If no list is given, use all of the owner's tasks."""
        pass

    def find_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of the owner's tasks whose time windows overlap."""
        pass
    