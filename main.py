from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def show(title: str, tasks: list[Task], scheduler: Scheduler) -> None:
    """Print a titled list of tasks."""
    print(f"\n{title}")
    print("-" * 60)
    if not tasks:
        print("  (none)")
        return
    for t in tasks:
        mark = "x" if t.completed else " "
        print(
            f"[{mark}] {t.time:%m/%d %I:%M %p}  {t.description:<16} "
            f"{scheduler.pet_name_for(t):<6} {t.frequency}"
        )


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

    # Added out of order on purpose. Vitamins and breakfast start at the same time.
    mochi.add_task(Task("Vet appointment", "appointment", at(14, 0), 60, "high"))
    buddy.add_task(Task("Breakfast", "feeding", at(8, 0), 15, "high", "daily"))
    buddy.add_task(Task("Morning walk", "walk", at(7, 30), 30, "high", "daily"))
    mochi.add_task(Task("Flea medication", "medication", at(8, 10), 5, "medium", "weekly"))
    mochi.add_task(Task("Vitamins", "medication", at(8, 0), 5, "low"))
    buddy.add_task(Task("Grooming", "appointment", at(10, 0, day_offset=1), 45, "low"))

    scheduler = Scheduler(owner)

    # Sorting
    show("All tasks, sorted by time", scheduler.sort_by_time(), scheduler)

    # Filtering
    show("Buddy's tasks only", scheduler.filter_tasks(pet_name="Buddy"), scheduler)
    show("Unfinished tasks", scheduler.filter_tasks(completed=False), scheduler)

    # Conflict detection (Breakfast and vitamins share a start time)
    print("\nConflict check")
    print("-" * 60)
    warnings = scheduler.get_conflict_warnings()
    if warnings:
        for warning in warnings:
            print(f"  ! {warning}")
    else:
        print("  No conflicts.")

    # Recurring tasks
    walk = next(t for t in buddy.tasks if t.description == "Morning walk")
    next_walk = scheduler.mark_task_complete(walk)
    print(f"\nMarked '{walk.description}' complete.")
    if next_walk:
        print(f"Next occurrence created for {next_walk.time:%m/%d %I:%M %p}.")
    show("Completed tasks", scheduler.filter_tasks(completed=True), scheduler)
    show("Buddy's tasks after completing the walk", scheduler.filter_tasks(pet_name="Buddy"), scheduler)


if __name__ == "__main__":
    main()

