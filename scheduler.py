# ai scheduling logic
from datetime import timedelta
def schedule_tasks(tasks):
    tasks = sorted(tasks, key=lambda t: t.deadline)
    schedule = []
    current_time = None
    for task in reversed(tasks):
        if current_time is None:
            current_time = task.deadline
        else:
            current_time = min(current_time, task.deadline)
        end_time = current_time
        start_time = end_time - timedelta(hours=task.duration)
        # Conflict detection 
        if start_time < task.deadline - timedelta(days=7):  
            print(f"Warning: Task {task.name} may not be schedulable")
        schedule.append((
            task.name,
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        current_time = start_time
    return list(reversed(schedule))