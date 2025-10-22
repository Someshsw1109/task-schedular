# src/task_scheduler.py

import heapq
from typing import Optional, List, Tuple

class TaskScheduler:
    """
    A task scheduler that orders tasks by an 'aging' priority.
    Core idea:
      - sort_prio = original_priority - floor(insertion_time / aging_interval)
      - heap stores (-sort_prio, remainder, counter, task_id)
      - at get_next: pop all entries sharing the same sort_prio,
        compute bonus = 0 if (t_insert % A) <= (t_now % A) else -1,
        pick the one with highest (sort_prio + bonus), tie-break by smallest counter.
    """

    def __init__(self, aging_interval: int = 10):
        if not isinstance(aging_interval, int) or aging_interval <= 0:
            raise ValueError("aging_interval must be a positive integer")
        self.aging_interval = aging_interval
        self._counter = 0  # monotonically increasing to break FIFO ties
        # Heap entries are: (–sort_prio, t_insert_mod, counter, task_id)
        self._tasks: List[Tuple[int, int, int, str]] = []

    def add_task(self, task_id: str, priority: int, timestamp: int) -> None:
        """
        Schedule a new task.

        Args:
          task_id: unique identifier
          priority: original integer priority
          timestamp: non-decreasing integer insertion time (seconds)
        """
        # Compute sort priority:
        sort_prio = priority - (timestamp // self.aging_interval)
        t_mod = timestamp % self.aging_interval
        heapq.heappush(
            self._tasks,
            (-sort_prio, t_mod, self._counter, task_id)
        )
        self._counter += 1

    def get_next(self, timestamp: int) -> Optional[str]:
        """
        Remove and return the task_id with highest effective priority at `timestamp`.
        Effective priority = sort_prio + bonus, where:
          bonus = 0 if (t_insert % A) <= (timestamp % A) else -1
        Tie-breaker for equal effective priority: earlier insertion (smaller counter).
        Returns None if no tasks remain.
        """
        if not self._tasks:
            return None

        # Pop the first group sharing the same sort_prio
        first = heapq.heappop(self._tasks)
        neg_sort, t_mod, cnt, tid = first
        tied = [first]
        while self._tasks and self._tasks[0][0] == neg_sort:
            tied.append(heapq.heappop(self._tasks))

        # Compute current remainder
        r_now = timestamp % self.aging_interval

        # Find the winner among 'tied'
        best = tied[0]
        best_key = None  # (effective_priority, -counter)
        for entry in tied:
            nsort, r_ins, ctr, t_id = entry
            sort_prio = -nsort
            bonus = 0 if r_ins <= r_now else -1
            eff_prio = sort_prio + bonus
            key = (eff_prio, -ctr)
            if best_key is None or key > best_key:
                best_key = key
                best = entry

        # Push losers back
        for entry in tied:
            if entry is not best:
                heapq.heappush(self._tasks, entry)

        # Return the winning task_id
        return best[3]