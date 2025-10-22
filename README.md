# Dynamic Task Scheduler  
**Difficulty:** Medium  

---

## Problem Overview

You are building a _dynamic_ Task Scheduler that orders tasks by an **aging priority**.  
Every task has:

- An **original priority** (integer).  
- An **insertion timestamp** (in seconds).  
- A shared **aging interval** _A_ (in seconds).

Over time, any waiting task’s effective priority increases by +1 for each full interval _A_ it has waited.

Your goal is to implement the **`TaskScheduler`** class (in `src/task_scheduler.py`) so that:

1. Inserting a task (`add_task`) takes O(log n) time.  
2. Retrieving the next task (`get_next`) also takes amortized O(log n) time.

---

## API Specification

Implement a Python class `TaskScheduler` with exactly these methods and signatures:

```python
class TaskScheduler:
    def __init__(self, aging_interval: int = 10):
        """
        aging_interval: number of seconds required for each task to gain +1 priority.
        """

    def add_task(self, task_id: str, priority: int, timestamp: int) -> None:
        """
        Schedule a new task.
        Args:
          task_id:   Unique identifier for this task.
          priority:  Initial integer priority.
          timestamp: The current time in seconds (non-decreasing across calls).
        """

    def get_next(self, timestamp: int) -> Optional[str]:
        """
        Remove and return the task_id with the highest _effective_ priority at `timestamp`.
        Effective priority = original_priority
                           + floor((timestamp – insertion_time) / aging_interval)

        Tie-breaking:
          • If two tasks share the same effective priority, return the one added earlier.
          • If no tasks remain, return None.
        """
```

---

## Example

```python
sched = TaskScheduler(aging_interval=10)
sched.add_task("A", priority=5, timestamp=0)
sched.add_task("B", priority=5, timestamp=0)

# At t=9: both have floor((9-0)/10)=0 → effective_priority=5
# Tie-breaker by insertion order → "A" wins
assert sched.get_next(9) == "A"

# Now only "B" remains.
# At t=20: floor((20-0)/10)=2 → effective_priority=5+2=7
assert sched.get_next(20) == "B"
```

---

## Notes

- The `timestamp` argument in `get_next` is provided for testing purposes only.  It will always be non-decreasing across calls.
- You may assume all input values are valid integers.
- add_task must run in O(log n).
- get_next should be amortized O(log n) even under high volume.

---
**Constraints:**

aging_interval is a positive integer.
priority and timestamp are non-negative integers.
Total number of tasks ≤ 10⁵ in any test.
All calls to add_task and get_next use non-decreasing timestamp.

---
**Provided Project Structure:**

```text
task-scheduler-problem/
├── Dockerfile
├── src/
│   ├── __init__.py      ← empty (needed for Python imports)
│   └── task_scheduler.py← stub to implement
└── tests/
    └── test_task_scheduler.py ← pytest unit tests
```

**Environment & Build**
We use Docker (Ubuntu 20.04 + Python 3.8 + pytest). The provided Dockerfile:

```Dockerfile
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Run the entire pytest suite; fail build if any test fails
RUN pytest --maxfail=1 --disable-warnings -q
```
---
**Building & Testing Locally**

**Install Docker Desktop (with WSL2) on Windows.**
Open PowerShell, cd into the project folder:
```PowerShell

cd path\to\task-scheduler-problem
```
Build the Docker image (this also runs tests):
```PowerShell

docker build -t task-scheduler-problem .
```
If the build succeeds, all tests passed and your implementation is correct.