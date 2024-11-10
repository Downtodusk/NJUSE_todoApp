import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from views.all_tasks_view import AllTasksView
from views.timeline_view import TimelineView
from views.add_task_view import AddTaskView
from views.today_tasks_view import TodayTasksView  # 导入 TodayTasksView
from data.task_storage import load_tasks, save_tasks

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f1f2f6")
        self.current_view = None

        # 当前选中按钮的引用
        self.selected_button = None

        # 左侧边栏
        self.sidebar = tk.Frame(self.root, width=220, bg="#2D3436", bd=0)
        self.sidebar.pack(side="left", fill="y")

        # 标题
        tk.Label(
            self.sidebar,
            text="TASK MANAGER",
            font=("Segoe UI", 16, "bold"),
            bg="#2D3436",
            fg="white",
        ).pack(pady=20)

        # 侧边栏按钮
        self.create_sidebar_button("📃 TODAY", self.show_today_tasks)
        self.create_sidebar_button("📆 ALL TASKS", self.show_all_tasks)
        self.create_sidebar_button("📍 TIMELINE", self.show_timeline)

        # 主内容区
        self.content = tk.Frame(self.root, bg="#ffffff", bd=0)
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # 添加任务按钮
        self.add_task_button = tk.Button(
            self.root,
            text="+ Add Task",
            font=("Segoe UI", 14, "bold"),
            bg="#0984e3",
            fg="white",
            bd=0,
            relief="flat",
            padx=15,
            pady=10,
            activebackground="#1d86e3",
            activeforeground="white",
            command=self.show_add_task
        )
        self.add_task_button.place(relx=0.85, rely=0.9, anchor="center")

        self.tasks = load_tasks()  # 从文件加载任务
        self.show_today_tasks()

        # 定时提醒
        self.root.after(1000, self.check_reminders)

    def create_sidebar_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 12),
            bg="#2D3436",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#1c1e21",
            activeforeground="white",
            command=lambda: self.on_sidebar_button_click(button, command),
        )
        button.pack(pady=10, fill="x", padx=20)

        # 添加悬停效果
        button.bind("<Enter>", lambda e: button.config(bg="#636e72" if button != self.selected_button else "#37474f"))
        button.bind("<Leave>", lambda e: button.config(bg="#2D3436" if button != self.selected_button else "#37474f"))

    def on_sidebar_button_click(self, button, command):
        """处理侧边栏按钮点击事件"""
        if self.selected_button:
            # 重置上一个选中按钮的样式
            self.selected_button.config(bg="#2D3436")
        # 更新当前选中按钮的样式
        button.config(bg="#37474f")
        self.selected_button = button
        command()

    def show_today_tasks(self):
        self.current_view = "today"
        self.clear_content()
        TodayTasksView(self.content, self.tasks, self.complete_task)

    def show_all_tasks(self):
        self.current_view = "all"
        self.clear_content()
        AllTasksView(self.content, self.tasks, self.complete_task)

    def show_timeline(self):
        self.current_view = "timeline"
        self.clear_content()
        TimelineView(self.content, self.tasks, self.complete_task)

    def show_add_task(self):
        self.clear_content()
        AddTaskView(self.content, self.add_task)

    def add_task(self, task):
        if task is not None:
            self.tasks.append(task)
            save_tasks(self.tasks)
        self.refresh_current_view()

    def complete_task(self, task):
        self.tasks.remove(task)
        save_tasks(self.tasks)
        self.refresh_current_view()

    def refresh_current_view(self):
        """根据当前视图刷新界面"""
        if self.current_view == "today":
            self.show_today_tasks()
        elif self.current_view == "all":
            self.show_all_tasks()
        elif self.current_view == "timeline":
            self.show_timeline()

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
