# task class
from datetime import datetime
class Task:
    def __init__(self, name, deadline, duration, dependencies):
        self.name = name
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        self.deadline_str = deadline
        self.duration = float(duration)
        self.dependencies = [d.strip() for d in dependencies if d.strip()]
        self.completed = False
    def urgency_score(self):
        now = datetime.now()
        time_left = (self.deadline - now).total_seconds() / 3600
        return time_left - self.duration
