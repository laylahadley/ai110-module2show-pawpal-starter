from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    now = datetime.now()

    def at(hour: int, minute: int = 0, day_offset: int = 0) -> datetime:
        """Build a datetime for today (or another day) at a given clock time."""
        return (now + timedelta(days=day_offset)).replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )

    owner = Owner(name="Jordan")
    buddy = Pet(name="Buddy", species="dog", age=4)
    mochi = Pet(name="Mochi", species="cat", age=2)
    owner.add_pet(buddy)
    owner.add_pet(mochi)

    # Added out of order on purpose, toshow that sorting works
    mochi.add_task(Task("Vet appointment", "appointment", at(14, 0), 60, "high"))
    buddy.add_task(Task("Breakfast", "feeding", at(8, 0), 15, "high"))
    buddy.add_task(Task("Morning walk", "walk", at(7, 30), 30, "high"))
    mochi.add_task(Task("Flea medication", "medication", at(8, 10), 5, "medium"))
    buddy.add_task(Task("Grooming", "appointment", at(10, 0, day_offset=1), 45, "low"))

    scheduler = Scheduler(owner)

    # Task has no pet field, so build a lookup for printing
    pet_of = {id(task): pet.name for pet in owner.pets for task in pet.tasks}

    print("=" * 52)
    print(f"Today's Schedule for {owner.name}")
    print("=" * 52)
    for task in scheduler.get_todays_tasks():
        mark = "x" if task.completed else " "
        print(
            f"[{mark}] {task.time:%I:%M %p}  {task.description:<16} "
            f"{pet_of[id(task)]:<6} {task.duration_minutes:>3} min  ({task.priority})"
        )

    conflicts = scheduler.find_conflicts()
    print()
    if conflicts:
        print("Conflicts detected:")
        for first, second in conflicts:
            print(
                f"  ! {first.description} ({pet_of[id(first)]}) overlaps "
                f"{second.description} ({pet_of[id(second)]})"
            )
    else:
        print("No conflicts.")


if __name__ == "__main__":
    main()

