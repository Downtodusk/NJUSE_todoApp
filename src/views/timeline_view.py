import tkinter as tk
from datetime import datetime

class TimelineView:
    def __init__(self, parent, tasks, complete_task_callback):
        self.parent = parent
        self.tasks = tasks
        self.complete_task_callback = complete_task_callback

        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(self.parent, bg="#f5f7fa", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)

        # 在 Canvas 中创建可滚动的 Frame
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f7fa")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 在 Canvas 宽度变化时动态更新任务框宽度
        self.canvas.bind("<Configure>", self.update_scrollable_frame_width)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # 显示任务列表
        self.display_tasks()

    def display_tasks(self):
        now = datetime.now()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            start_time = task['start_date']
            end_time = task['end_date']
            remaining_time = max(0, (end_time - now).total_seconds() // 3600)  # 剩余小时

            task_frame = tk.Frame(
                self.scrollable_frame,
                bg="#ffffff",
                relief="flat",
                bd=0,
                highlightbackground="#dddddd",
                highlightthickness=1,
                padx=10,
                pady=15
            )
            task_frame.pack(anchor="w", padx=10, pady=15, fill="x")

            # 任务标题和描述
            tk.Label(
                task_frame,
                text=task['title'],
                font=("Segoe UI", 16, "bold"),
                bg="#ffffff",
                fg="#333333"
            ).pack(anchor="w", pady=5)

            tk.Label(
                task_frame,
                text=task['description'],
                font=("Segoe UI", 12),
                bg="#ffffff",
                fg="#666666"
            ).pack(anchor="w", pady=10)

            # 显示剩余时间
            tk.Label(
                task_frame,
                text=f"Remaining: {remaining_time}h",
                font=("Segoe UI", 10, "bold"),
                bg="#ffffff",
                fg="#e74c3c" if remaining_time <= 2 else "#27ae60"  # 红色提示紧急，绿色正常
            ).pack(anchor="e", pady=5)

            # 显示时间范围
            time_frame = tk.Frame(task_frame, bg="#ffffff")
            time_frame.pack(anchor="w", pady=5)
            tk.Label(
                time_frame,
                text=f"Start: {start_time.strftime('%Y-%m-%d %H:%M')}",
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#555"
            ).pack(side="left", padx=(0, 10))

            tk.Label(
                time_frame,
                text=f"End: {end_time.strftime('%Y-%m-%d %H:%M')}",
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#e74c3c"
            ).pack(side="left")

            # 显示标签
            self.show_tags(task_frame, task['tags'])

            # 任务进度条
            self.add_progress_bar(task_frame, start_time, end_time, now)

            # 完成任务按钮
            complete_button = tk.Button(
                task_frame,
                text="✔ Mark as Done",
                command=lambda t=task: self.complete_task_callback(t),
                bg="#0984e3",
                fg="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=10,
                pady=5,
                activebackground="#3498db",
                activeforeground="white",
                borderwidth=0
            )
            complete_button.pack(side="right", padx=10, pady=5)

    def add_progress_bar(self, parent, start_time, end_time, now):
        """在任务框下方添加动态进度条"""
        progress_frame = tk.Frame(parent, bg="#ffffff")
        progress_frame.pack(fill="x", pady=(5, 10))

        # 计算进度
        total_duration = (end_time - start_time).total_seconds()
        elapsed_duration = (now - start_time).total_seconds()
        progress = min(max(elapsed_duration / total_duration, 0), 1)  # 进度百分比 (0-1)

        progress_canvas = tk.Canvas(progress_frame, height=15, bg="#e0e0e0", highlightthickness=0)
        progress_canvas.pack(fill="x", expand=True)

        # 在 Canvas 更新后绘制进度条
        progress_frame.update_idletasks()
        canvas_width = progress_canvas.winfo_width()
        progress_width = canvas_width * progress

        progress_color = self.get_progress_color(progress)
        progress_canvas.create_rectangle(0, 0, progress_width, 15, fill=progress_color, outline="")

    def get_progress_color(self, progress):
        """根据进度返回颜色（绿 -> 黄 -> 红）"""
        r = int(255 * progress)
        g = int(255 * (1 - progress))
        return f"#{r:02x}{g:02x}00"

    def show_tags(self, parent, tags):
        """为任务显示标签"""
        tag_colors = {"Study": "#ff9999", "Work": "#99ccff", "Private": "#99ff99"}
        tag_frame = tk.Frame(parent, bg="#ffffff")
        tag_frame.pack(anchor="w", pady=5)

        for tag in tags:
            color = tag_colors.get(tag, "#cccccc")
            tag_label = tk.Label(
                tag_frame,
                text=tag,
                bg=color,
                font=("Segoe UI", 10, "bold"),
                fg="#ffffff",
                padx=8,
                pady=3,
                relief="flat",
                bd=0
            )
            tag_label.pack(side="left", padx=5)

    def update_scrollable_frame_width(self, event):
        """更新 scrollable_frame 的宽度以适应 Canvas 宽度"""
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw"),
                               width=event.width)

    def on_mouse_wheel(self, event):
        """处理鼠标滚轮事件，调整 Canvas 的垂直位置"""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
