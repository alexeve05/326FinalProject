# ai scheduling logic
from datetime import timedelta
from csp import is_valid
def backtrack(tasks, schedule, index=0):
    if index == len(tasks):
        return schedule
    task = tasks[index]
    start = task.deadline - timedelta(hours=task.duration)
    while start <= task.deadline:
        if is_valid(task, start, schedule):
            schedule[task.name] = (
                start,
                start + timedelta(hours=task.duration)
            )
            result = backtrack(tasks, schedule, index + 1)
            if result:
                return result
            del schedule[task.name]
        start += timedelta(minutes=30)
    return None
def schedule_tasks(tasks):
    tasks = sorted(tasks, key=lambda t: t.deadline)
    schedule = {}
    result = backtrack(tasks, schedule)
    return result if result else {}