# AI Scheduling Assistant

# CS326 Final Project

## Author: Alexis Evans

### Features

- Add tasks with:
  - Name
  - Deadline
  - Duration
  - Dependencies
- CSV Import / Export support
- Task preview table (before scheduling)
- AI-based scheduling using CSP backtracking
- Conflict detection and failure explanation
- AI-generated suggestions for schedule improvement
- Task deletion (from UI or table)

### AI Techniques Used

- Constraint Satisfaction Problem (CSP)
- Backtracking search algorithm
- Heuristic-based suggestion system
- Conflict detection and explanation layer

### Project Structure

main.py → GUI + user interaction
models.py → Task data model
scheduler.py → CSP backtracking scheduler
csp.py → constraint validation functions
analysis.py → AI explanation + suggestions

---

### Requirements

- Python 3.9+
- No external libraries required (uses built-in Tkinter, csv, datetime)

### How to Run the Project

1. Extract the zip file
   Unzip the project folder.

2. Navigate to project directory

```bash
cd your-project-folder
```

3. Run program

   python main.py
