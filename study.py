import tkinter as tk
from tkinter import ttk
import json

FILE_PATH = "study_schedule.json"

# Load the JSON schedule
def load_schedule():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

# Save the JSON schedule
def save_schedule(schedule):
    with open(FILE_PATH, "w") as f:
        json.dump(schedule, f, indent=2)

# Main Application Class
class StudyTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Study Schedule Tracker")
        self.geometry("700x500")
        self.schedule = load_schedule()
        self.current_day_index = 0

        # UI Components
        self.date_label = ttk.Label(self, font=("Helvetica", 14, "bold"))
        self.task_frame = ttk.Frame(self)
        self.task_vars = []
        self.prev_button = ttk.Button(self, text="⏮ Previous", command=self.prev_day)
        self.next_button = ttk.Button(self, text="Next ⏭", command=self.next_day)
        self.save_button = ttk.Button(self, text="💾 Save Progress", command=self.save_progress)

        self.date_label.pack(pady=10)
        self.task_frame.pack(fill="both", expand=True, padx=20)
        self.prev_button.pack(side="left", padx=20, pady=10)
        self.save_button.pack(side="left", pady=10)
        self.next_button.pack(side="right", padx=20, pady=10)

        self.display_day()

    def display_day(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        self.task_vars = []

        day = self.schedule[self.current_day_index]
        self.date_label.config(text=f"{day['date']} - {day['hours']}h planned")

        for i, task in enumerate(day['tasks']):
            var = tk.BooleanVar(value=task['done'])
            cb = ttk.Checkbutton(self.task_frame, text=task['description'], variable=var)
            cb.pack(anchor="w", pady=3)
            self.task_vars.append(var)

    def save_progress(self):
        for i, var in enumerate(self.task_vars):
            self.schedule[self.current_day_index]['tasks'][i]['done'] = var.get()
        save_schedule(self.schedule)
        tk.messagebox.showinfo("Saved", "✅ Progress saved successfully!")

    def next_day(self):
        if self.current_day_index < len(self.schedule) - 1:
            self.current_day_index += 1
            self.display_day()

    def prev_day(self):
        if self.current_day_index > 0:
            self.current_day_index -= 1
            self.display_day()

# Run the App
if __name__ == "__main__":
    app = StudyTrackerApp()
    app.mainloop()
