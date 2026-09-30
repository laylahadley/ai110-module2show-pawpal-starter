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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
