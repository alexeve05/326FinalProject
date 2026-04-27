# runs gui
import datetime
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from collections import defaultdict
from tracemalloc import start
from models import Task
from scheduler import schedule_tasks
class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduler")
        self.tasks = []
        self.build_ui()
    def build_ui(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame = self.scrollable_frame
        # inputs
        self.name = self.create_input(frame, "Task Name")
        self.deadline = self.create_input(frame, "Deadline (YYYY-MM-DD HH:MM:SS)")
        self.duration = self.create_input(frame, "Duration (hours)")
        self.deps = self.create_input(frame, "Dependencies (comma-separated)")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="⚡ Generate Schedule", command=self.run_scheduler).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="🗑 Remove", command=self.remove_task).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="🧹 Clear", command=self.clear_all).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="📂 Import CSV", command=self.import_csv).grid(row=0, column=4, padx=5)
        # table
        self.tree = ttk.Treeview(frame, columns=("Deadline", "Duration"), show="headings")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Duration", text="Hours")
        self.tree.pack(fill="both", expand=True, pady=10)
        # calendar
        ttk.Label(frame, text="Calendar View").pack(anchor="w")
        self.calendar_frame = ttk.Frame(frame)
        self.calendar_frame.pack(fill="both", expand=True, pady=10)
        # output
        ttk.Label(frame, text="Schedule Log").pack(anchor="w")
        self.output = tk.Text(frame, height=10)
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
            self.tree.insert("", "end", iid=task.name, values=(task.deadline_str, task.duration))
            self.clear_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def clear_inputs(self):
        self.name.delete(0, tk.END)
        self.deadline.delete(0, tk.END)
        self.duration.delete(0, tk.END)
        self.deps.delete(0, tk.END)
    def remove_task(self):
        selected = self.tree.selection()
        for item in selected:
            self.tasks = [t for t in self.tasks if t.name != item]
            self.tree.delete(item)
    def clear_all(self):
        self.tasks.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.output.delete("1.0", tk.END)
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
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
                self.tree.insert("", "end", iid=task.name, values=(task.deadline_str, task.duration))
    def render_calendar(self, schedule):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        grouped = defaultdict(list)
        for task, start, end in schedule:
            day = start.split(" ")[0]
            grouped[day].append((task, start, end))
        row = col = 0
        for day in sorted(grouped.keys()):
            cell = ttk.Frame(self.calendar_frame, relief="ridge", padding=8)
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            ttk.Label(cell, text=f"📅 {day}", font=("Arial", 10, "bold")).pack(anchor="w")
            for task, start, end in grouped[day]:
                ttk.Label(cell, text=f"• {task}\n  {start.split()[1]} - {end.split()[1]}").pack(anchor="w")
            col += 1
            if col > 3:
                col = 0
                row += 1
    def run_scheduler(self):
        if not self.tasks:
            return
        schedule = schedule_tasks(self.tasks)
        self.output.delete("1.0", tk.END)
        if not schedule:
            messagebox.showerror("CSP Failure", "No valid schedule exists under constraints.")
            return
        for task, (start, end) in schedule.items():
            start_str = start.strftime("%Y-%m-%d %H:%M:%S")
            end_str = end.strftime("%Y-%m-%d %H:%M:%S")
            self.output.insert(tk.END, f"{task}: {start_str} → {end_str}\n")
            self.render_calendar([
            (task, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"))
            for task, (start, end) in schedule.items()
    ])
        for task, (start, end) in schedule.items():
            if end > self.tasks[0].deadline:
                messagebox.showwarning("Warning", f"{task} is tightly scheduled or near deadline")
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()