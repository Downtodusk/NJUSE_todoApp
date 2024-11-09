# views/all_tasks_view.py
import tkinter as tk

class AllTasksView:
    def __init__(self, parent, tasks):
        tk.Label(parent, text="All Tasks", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333").pack(pady=10)
        for task in tasks:
            tk.Label(parent, text=f"{task['title']} - {task['description']}", font=("Arial", 12), bg="#ffffff", fg="#555").pack(anchor="w", padx=10, pady=5)

    def show_tags(self, parent, tags):
        tag_colors = {"Study": "#ff9999", "Work": "#99ccff", "Private": "#99ff99"}
        for tag in tags:
            color = tag_colors.get(tag, "#cccccc")
            tk.Label(parent, text=tag, bg=color, font=("Arial", 10), padx=5, pady=2, relief="solid").pack(side="left",
                                                                                                          padx=2)