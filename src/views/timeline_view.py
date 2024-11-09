# views/timeline_view.py
import tkinter as tk

class TimelineView:
    def __init__(self, parent, tasks):
        tk.Label(parent, text="Timeline View", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333").pack(pady=10)
        for task in tasks:
            tk.Label(parent, text=f"{task['title']} - Due: {task['end_date']}", font=("Arial", 12), bg="#ffffff", fg="#555").pack(anchor="w", padx=10, pady=5)

