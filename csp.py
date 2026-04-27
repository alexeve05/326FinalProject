from datetime import timedelta
def overlaps(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1
def satisfies_dependencies(task, start_time, schedule):
    for dep in task.dependencies:
        if dep not in schedule:
            return False
        if schedule[dep][1] > start_time:
            return False
    return True
def satisfies_deadline(task, start_time):
    return start_time + timedelta(hours=task.duration) <= task.deadline
def no_conflicts(task, start_time, schedule):
    end_time = start_time + timedelta(hours=task.duration)
    for _, (s, e) in schedule.items():
        if overlaps(start_time, end_time, s, e):
            return False
    return True
def is_valid(task, start_time, schedule):
    return (
        satisfies_deadline(task, start_time)
        and satisfies_dependencies(task, start_time, schedule)
        and no_conflicts(task, start_time, schedule)
    )