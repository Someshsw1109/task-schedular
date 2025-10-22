# tests/test_task_scheduler.py
import pytest
from src.task_scheduler import TaskScheduler

@pytest.fixture
def scheduler():
    return TaskScheduler(aging_interval=10)

def test_simple_add_and_get(scheduler):
    scheduler.add_task("A", 5, timestamp=0)
    assert scheduler.get_next(timestamp=0) == "A"
    assert scheduler.get_next(timestamp=100) is None

def test_priority_order_without_aging(scheduler):
    scheduler.add_task("A", 5, timestamp=0)
    scheduler.add_task("B", 7, timestamp=0)
    assert scheduler.get_next(timestamp=0) == "B"
    assert scheduler.get_next(timestamp=0) == "A"

def test_aging_effect(scheduler):
    scheduler.add_task("A", 5, timestamp=0)
    scheduler.add_task("B", 5, timestamp=0)
    # At t=19, both have effective priority=5+1=6
    assert scheduler.get_next(timestamp=19) == "A"  # tie-breaker: A added earlier
    # Now only B remains; at t=20, effective priority=5+2=7
    assert scheduler.get_next(timestamp=20) == "B"

def test_mixed_aging_and_new_tasks(scheduler):
    scheduler.add_task("A", 1, timestamp=0)
    scheduler.add_task("B", 10, timestamp=5)
    # At t=15: A → 1+1=2, B →10+1=11 → B wins
    assert scheduler.get_next(timestamp=15) == "B"
    # Now only A remains; at t=25: A →1+2=3
    assert scheduler.get_next(timestamp=25) == "A"

def test_no_tasks(scheduler):
    assert scheduler.get_next(timestamp=50) is None

def test_multiple_get_calls(scheduler):
    scheduler.add_task("X", 2, timestamp=0)
    scheduler.add_task("Y", 2, timestamp=0)
    scheduler.add_task("Z", 2, timestamp=0)
    assert scheduler.get_next(timestamp=0) == "X"
    assert scheduler.get_next(timestamp=0) == "Y"
    assert scheduler.get_next(timestamp=0) == "Z"
    assert scheduler.get_next(timestamp=0) is None

def test_high_volume(scheduler):
    # 1000 tasks all with priority=0, inserted at t=0..999
    for i in range(1000):
        scheduler.add_task(f"T{i}", 0, timestamp=i)
    # At t=10000, every task got +floor((10000−i)/10) ≥ +999 → same effective priority
    # They should come out in insertion order
    for i in range(1000):
        assert scheduler.get_next(timestamp=10000) == f"T{i}"
    assert scheduler.get_next(timestamp=20000) is None