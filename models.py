# task class
from datetime import datetime
class Task:
    def __init__(self, name, deadline, duration, priority, dependencies):
        self.name = name
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
        self.duration = float(duration)
        self.priority = int(priority)
        self.dependencies = dependencies
        self.scheduled_day = None
