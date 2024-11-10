# main_view.py
import tkinter as tk
from datetime import datetime, timedelta, date
from tkinter import messagebox
from views.all_tasks_view import AllTasksView
from views.timeline_view import TimelineView
from views.add_task_view import AddTaskView
from views.today_tasks_view import TodayTasksView  # 导入 TodayTasksView
from data.task_storage import load_tasks, save_tasks

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management - Main View")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        # 左侧边栏
        self.sidebar = tk.Frame(self.root, width=150, bg="#0c87d4")
        self.sidebar.pack(side="left", fill="y")

        tk.Button(self.sidebar, text="📃TODAY", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_today_tasks).pack(pady=20, fill="x")
        tk.Button(self.sidebar, text="📆 ALL", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_all_tasks).pack(pady=20, fill="x")
        tk.Button(self.sidebar, text="📍TIMELINE", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_timeline).pack(pady=20, fill="x")

        # 主内容区
        self.content = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.content.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # 添加任务按钮
        self.add_task_button = tk.Button(self.root, text="Add Task", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_add_task)
        self.add_task_button.place(relx=0.85, rely=0.9, anchor="center")

        self.tasks = load_tasks()  # 从文件加载任务
        self.show_today_tasks()

        # 定时提醒
        self.root.after(1000, self.check_reminders)

    def show_today_tasks(self):
        self.clear_content()
        TodayTasksView(self.content, self.tasks, self.complete_task)

    def show_all_tasks(self):
        self.clear_content()
        AllTasksView(self.content, self.tasks, self.complete_task)

    def show_timeline(self):
        self.clear_content()
        TimelineView(self.content, self.tasks, self.complete_task)

    def show_add_task(self):
        self.clear_content()
        AddTaskView(self.content, self.add_task)

    def add_task(self, task):
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.show_today_tasks()

    def complete_task(self, task):
        self.tasks.remove(task)
        save_tasks(self.tasks)
        self.show_today_tasks()

    def check_reminders(self):
        now = datetime.now()
        for task in self.tasks:
            if task["reminder_time"] and now >= task["reminder_time"]:
                messagebox.showinfo("Reminder", f"Reminder for Task: {task['title']}")
                if task["reminder_repeats"] > 0:
                    task["reminder_repeats"] -= 1
                    task["reminder_time"] += timedelta(minutes=5)
                else:
                    task["reminder_time"] = None
        self.root.after(1000, self.check_reminders)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
