from collections import defaultdict
def detect_conflicts(tasks):
    issues = []
    names = {t.name for t in tasks}
    for t in tasks:
        for d in t.dependencies:
            if d not in names:
                issues.append(f"'{t.name}' depends on missing task '{d}'")
    return issues
def generate_suggestions(tasks):
    suggestions = []
    if not tasks:
        return ["No tasks provided"]
    longest = max(tasks, key=lambda t: t.duration)
    suggestions.append(
        f"Consider starting '{longest.name}' earlier due to long duration"
    )
    tight = [t for t in tasks if t.duration > 3]
    if len(tight) > 2:
        suggestions.append(
            "Multiple long tasks detected → consider splitting workload across days"
        )
    complex_tasks = [t for t in tasks if len(t.dependencies) > 1]
    for t in complex_tasks:
        suggestions.append(
            f"'{t.name}' has multiple dependencies → may cause scheduling bottlenecks"
        )
    return suggestions
def explain_failure(tasks):
    conflicts = detect_conflicts(tasks)
    if not conflicts:
        return ["Schedule failed due to tight time constraints or overlap density"]
    return conflicts