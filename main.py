# runs gui
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from models import Task
from scheduler import schedule_tasks
from analysis import generate_suggestions, explain_failure
class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Scheduling Assistant")
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
        self.name = self.create_input(frame, "Task Name")
        self.deadline = self.create_input(frame, "Deadline (YYYY-MM-DD HH:MM:SS)")
        self.duration = self.create_input(frame, "Duration (hours)")
        self.deps = self.create_input(frame, "Dependencies (comma-separated)")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0)
        ttk.Button(btn_frame, text="🗑 Delete Task", command=self.delete_task).grid(row=0, column=1)
        ttk.Button(btn_frame, text="⚡ Run AI Scheduler", command=self.run_scheduler).grid(row=0, column=2)
        ttk.Button(btn_frame, text="📂 Import CSV", command=self.import_csv).grid(row=0, column=3)
        ttk.Button(btn_frame, text="💾 Export CSV", command=self.export_csv).grid(row=0, column=4)
        ttk.Label(frame, text="📋 Task Preview (Before Scheduling)").pack(anchor="w")
        self.task_table = ttk.Treeview(
            frame,
            columns=("Name", "Deadline", "Duration", "Dependencies"),
            show="headings"
        )
        self.task_table.heading("Name", text="Task")
        self.task_table.heading("Deadline", text="Deadline")
        self.task_table.heading("Duration", text="Hours")
        self.task_table.heading("Dependencies", text="Dependencies")
        self.task_table.pack(fill="both", expand=True, pady=10)
        self.output = tk.Text(frame, height=15)
        self.output.pack(fill="both", expand=True)
    def create_input(self, parent, label):
        ttk.Label(parent, text=label).pack(anchor="w")
        entry = ttk.Entry(parent)
        entry.pack(fill="x")
        return entry
    def refresh_task_view(self):
        self.task_table.delete(*self.task_table.get_children())
        for t in self.tasks:
            self.task_table.insert(
                "",
                "end",
                values=(
                    t.name,
                    t.deadline_str,
                    t.duration,
                    ",".join(t.dependencies)
                )
            )
    def clear_inputs(self):
        self.name.delete(0, tk.END)
        self.deadline.delete(0, tk.END)
        self.duration.delete(0, tk.END)
        self.deps.delete(0, tk.END)
    def add_task(self):
        try:
            task = Task(
                self.name.get(),
                self.deadline.get(),
                float(self.duration.get()),
                self.deps.get().split(",") if self.deps.get() else []
            )
            self.tasks.append(task)
            self.refresh_task_view()
            self.clear_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def delete_task(self):
        selected = self.task_table.selection()
        if selected:
            for item in selected:
                values = self.task_table.item(item, "values")
                name = values[0]
                self.tasks = [t for t in self.tasks if t.name != name]
        else:
            selected_name = self.name.get().strip()
            if not selected_name:
                messagebox.showwarning("Delete Task", "Select a task or enter a name")
                return
            self.tasks = [t for t in self.tasks if t.name != selected_name]
        self.refresh_task_view()
        self.clear_inputs()
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "deadline", "duration", "dependencies"])
            for t in self.tasks:
                writer.writerow([
                    t.name,
                    t.deadline_str,
                    t.duration,
                    ",".join(t.dependencies)
                ])
        messagebox.showinfo("Export Complete", "Tasks exported successfully!")
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        self.tasks.clear()
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                task = Task(
                    row["name"],
                    row["deadline"],
                    float(row["duration"]),
                    row["dependencies"].split(",") if row.get("dependencies") else []
                )
                self.tasks.append(task)
        self.refresh_task_view()
        messagebox.showinfo("Import Complete", "Tasks loaded successfully!")
    def run_scheduler(self):
        self.output.delete("1.0", tk.END)
        result = schedule_tasks(self.tasks)
        if result["status"] == "success":
            self.output.insert(tk.END, "✅ AI Generated Schedule:\n\n")
            for task, (start, end) in result["schedule"].items():
                self.output.insert(tk.END, f"{task}: {start} → {end}\n")
            self.output.insert(tk.END, "\n💡 AI Suggestions:\n")
            for s in generate_suggestions(self.tasks):
                self.output.insert(tk.END, f"- {s}\n")
        else:
            self.output.insert(tk.END, "❌ No valid schedule found\n\n")
            self.output.insert(tk.END, "🧠 AI Diagnosis:\n")
            for c in explain_failure(self.tasks):
                self.output.insert(tk.END, f"- {c}\n")
            self.output.insert(tk.END, "\n💡 Suggested Fixes:\n")
            for s in generate_suggestions(self.tasks):
                self.output.insert(tk.END, f"- {s}\n")
# RUN APP
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()