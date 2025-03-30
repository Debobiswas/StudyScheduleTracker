
import tkinter as tk
from tkinter import ttk, messagebox
import json

FILE_PATH = "study_schedule.json"

def load_schedule():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_schedule(schedule):
    with open(FILE_PATH, "w") as f:
        json.dump(schedule, f, indent=2)

class StudyTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Study Schedule Tracker")
        self.geometry("800x600")
        self.configure(bg="#f0f4f8")
        self.schedule = load_schedule()
        self.current_day_index = 0
        self.task_vars = []

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#f0f4f8")
        self.style.configure("TButton", font=("Segoe UI", 11))
        self.style.configure("Task.TCheckbutton", font=("Segoe UI", 11), background="#f0f4f8")

        self.build_ui()

    def build_ui(self):
        header = ttk.Label(self, text="📚 Study Tracker", font=("Segoe UI", 20, "bold"), foreground="#3b82f6")
        header.pack(pady=10)

        self.date_label = ttk.Label(self, font=("Segoe UI", 14, "bold"))
        self.date_label.pack(pady=5)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg="#f0f4f8", highlightthickness=0)
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

        self.progress_label = ttk.Label(self, text="", font=("Segoe UI", 11))
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=600, mode="determinate")
        self.progress_bar.pack(pady=5)

        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=10)

        self.prev_button = ttk.Button(nav_frame, text="⏮ Previous", command=self.prev_day)
        self.save_button = ttk.Button(nav_frame, text="💾 Save Progress", command=self.save_progress)
        self.next_button = ttk.Button(nav_frame, text="Next ⏭", command=self.next_day)

        self.prev_button.grid(row=0, column=0, padx=10)
        self.save_button.grid(row=0, column=1, padx=10)
        self.next_button.grid(row=0, column=2, padx=10)

        self.display_day()

    def display_day(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.task_vars = []

        day = self.schedule[self.current_day_index]
        self.date_label.config(text=f"{day['date']} - {day['hours']}h planned")

        for i, task in enumerate(day['tasks']):
            var = tk.BooleanVar(value=task['done'])
            cb = ttk.Checkbutton(self.scrollable_frame, text=task['description'], variable=var, style="Task.TCheckbutton")
            cb.pack(anchor="w", pady=3)
            self.task_vars.append(var)

        self.update_progress_bar()

    def update_progress_bar(self):
        done = sum(1 for v in self.task_vars if v.get())
        total = len(self.task_vars)
        percent = int((done / total) * 100) if total else 0
        self.progress_bar["value"] = percent
        self.progress_label.config(text=f"Progress: {percent}% ({done}/{total} tasks done)")

    def save_progress(self):
        for i, var in enumerate(self.task_vars):
            self.schedule[self.current_day_index]['tasks'][i]['done'] = var.get()
        save_schedule(self.schedule)
        self.update_progress_bar()
        messagebox.showinfo("Saved", "✅ Progress saved successfully!")

    def next_day(self):
        if self.current_day_index < len(self.schedule) - 1:
            self.save_progress()
            self.current_day_index += 1
            self.display_day()

    def prev_day(self):
        if self.current_day_index > 0:
            self.save_progress()
            self.current_day_index -= 1
            self.display_day()

if __name__ == "__main__":
    app = StudyTrackerApp()
    app.mainloop()
