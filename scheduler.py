# ai scheduling logic
from datetime import timedelta
def schedule_tasks(tasks):
    tasks = sorted(tasks, key=lambda t: t.deadline)
    schedule = []
    for task in tasks:
        end_time = task.deadline
        start_time = end_time - timedelta(hours=task.duration)
        schedule.append((
            task.name,
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
    return schedule