import tkinter as tk
from views.all_tasks_view import AllTasksView
from views.timeline_view import TimelineView
from views.add_task_view import AddTaskView  # 导入添加任务视图
from datetime import date

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management - Main View")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        # 左侧边栏
        self.sidebar = tk.Frame(self.root, width=150, bg="#0c87d4")
        self.sidebar.pack(side="left", fill="y")

        tk.Button(self.sidebar, text="Today's Tasks", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_today_tasks).pack(pady=20, fill="x")
        tk.Button(self.sidebar, text="All Tasks", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_all_tasks).pack(pady=20, fill="x")
        tk.Button(self.sidebar, text="Timeline", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_timeline).pack(pady=20, fill="x")

        # 主内容区
        self.content = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.content.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # 添加任务按钮，放置在右下角
        self.add_task_button = tk.Button(self.root, text="Add Task", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, command=self.show_add_task)
        self.add_task_button.place(relx=0.85, rely=0.9, anchor="center")  # 定位在右下角

        self.tasks = []  # 存储所有任务
        self.show_today_tasks()

    def show_today_tasks(self):
        self.clear_content()
        tk.Label(self.content, text="Today's Tasks", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333").pack(pady=10)
        today_tasks = [task for task in self.tasks if task['start_date'] == date.today()]
        for task in today_tasks:
            task_frame = tk.Frame(self.content, bg="#ffffff", relief="solid", bd=2, padx=10, pady=5)
            task_frame.pack(anchor="w", padx=10, pady=5, fill="x")

            # 任务标题和描述
            tk.Label(task_frame, text=f"{task['title']} - {task['description']}", font=("Arial", 12), bg="#ffffff", fg="#555").pack(anchor="w", pady=5)

            # 显示标签
            self.show_tags(task_frame, task['tags'])

            # 横线分隔
            tk.Frame(self.content, height=1, bg="#D3D3D3").pack(fill="x", pady=5)

    def show_tags(self, parent, tags):
        """为任务显示标签"""
        tag_colors = {"Study": "#ff9999", "Work": "#99ccff", "Private": "#99ff99"}
        tag_frame = tk.Frame(parent, bg="#ffffff")
        tag_frame.pack(anchor="w", pady=5)

        for tag in tags:
            color = tag_colors.get(tag, "#cccccc")  # 默认颜色为灰色
            tag_label = tk.Label(tag_frame, text=tag, bg=color, font=("Arial", 10), padx=5, pady=2, relief="solid", bd=1)
            tag_label.pack(side="left", padx=5)

    def show_all_tasks(self):
        self.clear_content()
        AllTasksView(self.content, self.tasks)  # 将所有任务列表传递给视图

    def show_timeline(self):
        self.clear_content()
        TimelineView(self.content, self.tasks)  # 传递任务列表到时间线视图

    def show_add_task(self):
        self.clear_content()
        AddTaskView(self.content, self.add_task)  # 将添加任务视图和回调传递给视图

    def add_task(self, task):
        """添加任务并刷新显示"""
        self.tasks.append(task)  # 将新任务添加到任务列表
        self.show_today_tasks()  # 更新主界面显示的任务

    def clear_content(self):
        """清空主界面内容"""
        for widget in self.content.winfo_children():
            widget.destroy()
