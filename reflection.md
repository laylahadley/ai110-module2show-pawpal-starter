# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform:

1. add a pet to their profile.
2. schedule a care task (feeding, walk, medication, appointment) for a pet.
3. view today's tasks in time order and see any scheduling conflicts. 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    - My initial design has four classes. Task is a dataclass holding one care activity (description, category, time, duration, priority, frequency, completed) and can mark itself complete. Pet is a dataclass holding the pet's basic info and its list of tasks. Owner holds the owner's name and their pets and can gather every task across all pets. Scheduler takes an Owner and is responsible for the logic: getting today's tasks, sorting by time, and detecting conflicts.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    - After asking the AI to review my skeleton, I made these changes:
        - Changed Task.time from a string to a datetime. Strings like "9:00" and "10:00" sort incorrectly and can't be used to detect overlaps. A datetime also carries the date, which get_todays_tasks() needs.
        - Made Scheduler.sort_by_time() and find_conflicts() work from self.owner.get_all_tasks() by default, so the Scheduler has one source of truth for tasks.
        - Changed find_conflicts() to return pairs of tasks, so it's clear which tasks conflict.
        
        I decided not to add owner constraints (like available time or preferences) yet. The scheduler doesn't enforce them, so adding them now would be unnecessary complexity. I can add them later if the scheduling logic needs them.
---

## 2. Scheduling Logic and Tradeoffs
- One tradeoff my scheduler makes is how it handles conflicts. find_conflicts() detects overlapping time windows (start time plus duration), which is more accurate than only checking for exact matching start times, but it only reports warnings. It does not block the user or reschedule anything. It also checks across all pets, because one owner has to do every task, but it ignores travel time or setup time between tasks. I kept this simple because a pet owner can fix a warning faster than an automatic reshuffle would, and a simpler algorithm is easier to read and trust.

When the AI suggested a more readable version of find_conflicts(), I kept my version. It was already reasonably efficient b/c it sorts tasks once and stops checking later tasks when their start time is after the current task's end time.


**a. Constraints and priorities**

My scheduler considers five things: **start time** (each task is a datetime, so it knows both the date and the time of day), **duration** (used to work out whether two tasks overlap), **frequency** (once, daily, or weekly, which decides whether completing a task creates another one), **completion status** (finished tasks are skipped by conflict detection and can be filtered), and **which pet** a task belongs to (used for filtering and for naming pets in warnings). Tasks also carry a **priority** (low, medium, or high). Priority is stored and shown in the UI, but the scheduler does not yet use it to order or drop tasks. Owner preferences and available time are not modeled.

I decided time mattered most because pet care is time-bound: medications, meals, and walks have to happen at particular times, and one owner can't do two things at once. Time and duration are what make conflict detection possible. I treated priority as secondary because it only matters when the scheduler has to choose between tasks, and mine warns instead of choosing. I left owner preferences out because nothing in the scheduler would enforce them yet, a call I made during the design review in section 1b.

**b. Tradeoffs**

My scheduler detects conflicts by checking whether task time windows (start time plus duration) overlap, and it only reports warnings. It does not block the owner or reschedule anything. It also compares tasks across all pets, since one owner has to do all of them, but it ignores travel or setup time between tasks.

This is reasonable for the scenario because the owner knows things the scheduler doesn't (for example, feeding one pet while another is finishing a walk). An automatic reshuffle could quietly move a medication or vet appointment. A warning is simple to understand, easy to test, and leaves the decision with the owner. Checking overlapping windows instead of only exact start times catches more real problems, and because tasks are sorted first, the check can stop early for each task instead of comparing every pair.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant at essentially each stage. For design, I listed my classes and asked it to draft a Mermaid UML diagram, then had it review my class skeleton for missing relationships and bottlenecks. For implementation, I used it to turn the skeleton into working code and to brainstorm which algorithms to add (sorting, filtering, recurrence, conflict detection). For testing, I used it to draft pytest tests and to explain tests I didn't understand before saving them. 

The most helpful prompts were specific and gave it constraints: attaching the actual file, naming the classes and method signatures to keep, and saying things like "keep it simple, don't include any extra classes." Review-style questions such as "what relationships or logic bottlenecks am I missing?" were more useful than open-ended "write this for me" requests, because they gave me concrete things to accept or reject. Addionally, starting a new chat for each phase (implementation, algorithms, testing) also kept each conversation focused on one job.

**b. Judgment and verification**

When the AI reviewed my skeleton, it suggested adding owner constraints such as available time and preferences to the Owner class. I did not end up accepting that, because nothing in my scheduler enforced them, and unused attributes would have made the design more complicated without making it do anything more. I accepted its other suggestions (storing `Task.time` as a real datetime instead of a string, making the Scheduler work from the owner's tasks, and returning conflicting pairs) because each one fixed a specific problem I could point to: strings like "9:00" and "10:00" sort incorrectly, and a scheduler with its own separate task list could disagree with the owner's data.

I evaluated suggestions by asking whether they solved a real problem in my design, then checking the result by running it. I ran `main.py` with tasks added out of order and with two tasks at the same time, compared the printed output to what I expected, and wrote automated tests so the behavior could be rechecked after every change.

---

## 4. Testing and Verification

**a. What you tested**

I wrote [15] pytest tests covering the core behaviors: sorting returns tasks in chronological order even when they were added out of order; filtering by pet and by completion status works; completing a daily task creates one for the next day, a weekly task creates one a week later, and a one-time task creates nothing; conflict detection flags tasks with the same start time and overlapping durations, does not flag back-to-back tasks, and ignores completed tasks; and edge cases such as pets with no tasks and "today's tasks" excluding other days. These mattered because they are the behaviors the app's features depend on. Conflict detection and recurrence are where off-by-one mistakes are easy to make (e.g.: treating a task that ends exactly when another starts as a conflict), so I tested those boundaries on purpose.

**b. Confidence**

I'm fairly confident (4 out of 5 stars) that the scheduler works correctly for the behaviors I tested, since all the tests pass and I checked the same behavior by hand in the CLI demo and the Streamlit app. I held back one star because the Streamlit UI has no automated tests and some edge cases remain untested.

With more time, I would maybe test duplicate pet names, recurring tasks completed long after their due date (the next occurrence would land in the past), zero-length or very long durations, daylight saving time changes, and invalid input in the UI.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with building the logic layer first and verifying it in the terminal and with tests before connecting the Streamlit UI. When I connected the UI, the classes already worked, so I only had to debug the wiring and not the logic. I'm also satisfied with the recurrence and conflict-detection features, since they turned a basic task list into something that actually helps an owner plan a day.

**b. What you would improve**

I would make the scheduler use priority, for example to order tasks that start at the same time or to suggest which task to move when there's a conflict. I would also add owner preferences and available time windows, now that there's a scheduler that could enforce them. On the design side, tasks currently don't know which pet they belong to, so the scheduler has to search each pet's list to find out, and giving `Task` a reference to its pet would be cleaner. Lastly, data disappears when the browser refreshes, so I would save pets and tasks to a file.

**c. Key takeaway**

My main takeaway is that being the 'lead architect' means owning the design, not just accepting code. The AI was fast at producing code, but it didn't decide what the system should be. I set the classes and responsibilities, chose suggestions to take or reject, and used tests to check what the code actually did instead of trusting what the AI said it did. Keeping the design small and clear at the start also made the AI's output much better in every later phase.