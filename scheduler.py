# ai scheduling logic
from collections import defaultdict, deque
from datetime import datetime, timedelta
def topological_sort(tasks):
    graph = defaultdict(list)
    indegree = defaultdict(int)
    task_map = {t.name: t for t in tasks if not t.completed}
    for t in task_map.values():
        for dep in t.dependencies:
            if dep in task_map:
                graph[dep].append(t.name)
                indegree[t.name] += 1
    queue = deque([t.name for t in task_map.values() if indegree[t.name] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(task_map[node])
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != len(task_map):
        raise Exception("Dependency cycle detected or missing dependency")
    return order
def schedule_tasks(tasks, hours_per_day=6, start_date="2026-04-25"):
    tasks = [t for t in tasks if not t.completed]
    tasks = topological_sort(tasks)
    tasks.sort(key=lambda t: (t.urgency_score(), t.duration))
    current_day = datetime.strptime(start_date, "%Y-%m-%d")
    remaining_hours = hours_per_day
    schedule = []
    for task in tasks:
        while task.duration > remaining_hours:
            current_day += timedelta(days=1)
            remaining_hours = hours_per_day
        schedule.append((task.name, current_day.strftime("%Y-%m-%d")))
        remaining_hours -= task.duration
    return schedule