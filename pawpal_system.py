from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    category: str
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str, pets: list[Pet] | None = None) -> None:
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_todays_tasks(self) -> list[Task]:
        pass

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        pass

    def find_conflicts(self, tasks: list[Task]) -> list[Task]:
        pass
