import tkinter as tk
from datetime import date

class TodayTasksView:
    def __init__(self, parent, tasks, complete_task_callback):
        self.parent = parent
        self.tasks = tasks
        self.complete_task_callback = complete_task_callback  # 完成任务的回调

        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(self.parent, bg="#ffffff")
        self.scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)

        # 在 Canvas 中创建可滚动的 Frame
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff")

        # 让 scrollable_frame 填满 Canvas 的宽度
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 将 scrollable_frame 添加到 Canvas 中并设置宽度绑定
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())

        # 配置 Canvas 和 Scrollbar 的布局
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 在 Canvas 宽度变化时动态更新任务框宽度
        self.canvas.bind("<Configure>", self.update_scrollable_frame_width)

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # 显示任务列表
        self.display_today_tasks()

    def display_today_tasks(self):
        today = date.today()
        today_tasks = [task for task in self.tasks if task['start_date'].date() == today]

        for i, task in enumerate(today_tasks, start=1):
            task_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="solid", bd=2, padx=10, pady=5)
            task_frame.pack(anchor="w", padx=10, pady=5, fill="x")

            # 任务标题和描述
            tk.Label(task_frame, text=f"{task['title']} - {task['description']}", font=("Arial", 12), bg="#ffffff", fg="#555").pack(anchor="w", pady=5)

            # 标签显示
            self.show_tags(task_frame, task['tags'])

            # 添加“完成”按钮
            complete_button = tk.Button(task_frame, text="Mark as Done", command=lambda t=task: self.complete_task_callback(t), bg="#28a745", fg="white", font=("Arial", 10), relief="flat")
            complete_button.pack(side="right", padx=10, pady=5)

    def show_tags(self, parent, tags):
        """为任务显示标签"""
        tag_colors = {"Study": "#ff9999", "Work": "#99ccff", "Private": "#99ff99"}
        tag_frame = tk.Frame(parent, bg="#ffffff")
        tag_frame.pack(anchor="w", pady=5)

        for tag in tags:
            color = tag_colors.get(tag, "#cccccc")  # 默认颜色为灰色
            tag_label = tk.Label(tag_frame, text=tag, bg=color, font=("Arial", 10), padx=5, pady=2, relief="solid", bd=1)
            tag_label.pack(side="left", padx=5)

    def update_scrollable_frame_width(self, event):
        """更新 scrollable_frame 的宽度以适应 Canvas 宽度"""
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw"),
                               width=event.width)

    def on_mouse_wheel(self, event):
        """鼠标滚轮滚动事件，调整 Canvas 的垂直位置"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
