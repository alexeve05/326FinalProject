# runs gui
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from collections import defaultdict
from models import Task
from scheduler import schedule_tasks
class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduler ✨")
        self.tasks = []
        self.build_ui()
    def build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)
# Inputs
        self.name = self.create_input(frame, "Task Name")
        self.deadline = self.create_input(frame, "Deadline (YYYY-MM-DD HH:MM:SS)")
        self.duration = self.create_input(frame, "Duration (hours)")
        self.deps = self.create_input(frame, "Dependencies (comma-separated)")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Generate Schedule", command=self.run_scheduler).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="📂 Import CSV", command=self.import_csv).grid(row=0, column=3, padx=5)
# Task Table
        self.tree = ttk.Treeview(frame, columns=("Deadline", "Duration", "Status"), show="headings")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Duration", text="Hours")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True, pady=10)
# Calendar Section
        ttk.Label(frame, text="Calendar View").pack(anchor="w")
        self.calendar_frame = ttk.Frame(frame)
        self.calendar_frame.pack(fill="both", expand=True, pady=10)
# Text fallback output
        ttk.Label(frame, text="Schedule Log").pack(anchor="w")
        self.output = tk.Text(frame, height=8)
        self.output.pack(fill="both", expand=True)
    def create_input(self, parent, label):
        ttk.Label(parent, text=label).pack(anchor="w")
        entry = ttk.Entry(parent)
        entry.pack(fill="x", pady=3)
        return entry
    def add_task(self):
        try:
            task = Task(
                self.name.get(),
                self.deadline.get(),
                float(self.duration.get()),
                self.deps.get().split(",") if self.deps.get() else []
            )
            self.tasks.append(task)
            self.tree.insert("", "end", iid=task.name, values=(
                task.deadline_str,
                task.duration,
                "Pending"
            ))
            self.clear_inputs()
        except Exception as e:
            messagebox.showerror("Invalid Input", str(e))
    def clear_inputs(self):
        self.name.delete(0, tk.END)
        self.deadline.delete(0, tk.END)
        self.duration.delete(0, tk.END)
        self.deps.delete(0, tk.END)
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    task = Task(
                        row["name"],
                        row["deadline"],
                        float(row["duration"]),
                        row.get("dependencies", "").split(",") if row.get("dependencies") else []
                    )
                    self.tasks.append(task)
                    self.tree.insert("", "end", iid=task.name, values=(
                        task.deadline_str,
                        task.duration,
                        "Pending"
                    ))
            messagebox.showinfo("Success", "CSV Imported Successfully!")
        except Exception as e:
            messagebox.showerror("CSV Error", str(e))
    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Task", "Select a task first")
            return
        for item in selected:
            for t in self.tasks:
                if t.name == item:
                    t.completed = True
            self.tree.set(item, "Status", "Completed")
    def render_calendar(self, schedule):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        grouped = defaultdict(list)
        for task, day in schedule:
            grouped[day].append(task)
        row = 0
        col = 0
        for day in sorted(grouped.keys()):
            cell = ttk.Frame(self.calendar_frame, relief="ridge", padding=8)
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            ttk.Label(cell, text=f"📅 {day}", font=("Arial", 10, "bold")).pack(anchor="w")
            for task in grouped[day]:
                ttk.Label(cell, text=f"• {task}").pack(anchor="w")
            col += 1
            if col > 3:  # 4 columns per row
                col = 0
                row += 1
    def run_scheduler(self):
        if not self.tasks:
            messagebox.showwarning("No tasks", "Add or import tasks first!")
            return
        try:
            schedule = schedule_tasks(self.tasks)
# Text log
            self.output.delete("1.0", tk.END)
            current_day = None
            for task, day in schedule:
                if day != current_day:
                    self.output.insert(tk.END, f"\n📅 {day}\n")
                    current_day = day
                self.output.insert(tk.END, f"   • {task}\n")
# Calendar grid view
            self.render_calendar(schedule)
        except Exception as e:
            messagebox.showerror("Scheduling Error", str(e))
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()