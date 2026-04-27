# ai scheduling logic
from collections import defaultdict, deque
from datetime import datetime, timedelta
def topological_sort(tasks):
    graph = defaultdict(list)
    indegree = defaultdict(int)
    task_map = {t.name: t for t in tasks}
    for task in tasks:
        for dep in task.dependencies:
            graph[dep].append(task.name)
            indegree[task.name] += 1
    queue = deque([t.name for t in tasks if indegree[t.name] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(task_map[node])
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order
def schedule_tasks(tasks, hours_per_day=6, start_date="2026-04-25"):
    tasks = topological_sort(tasks)
    current_day = datetime.strptime(start_date, "%Y-%m-%d")
    remaining_hours = hours_per_day
    schedule = []
    for task in tasks:
        if task.duration > remaining_hours:
            current_day += timedelta(days=1)
            remaining_hours = hours_per_day
        task.scheduled_day = current_day.strftime("%Y-%m-%d")
        schedule.append((task.name, task.scheduled_day))
        remaining_hours -= task.duration
    return schedule