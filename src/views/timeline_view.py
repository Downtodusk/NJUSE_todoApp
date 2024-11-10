import tkinter as tk


class TimelineView:
    def __init__(self, parent, tasks, complete_task_callback):
        self.parent = parent
        self.tasks = tasks
        self.complete_task_callback = complete_task_callback  # 完成任务的回调

        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(self.parent, bg="#f5f7fa", highlightthickness=0)  # 使用浅灰色背景
        self.scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)

        # 在 Canvas 中创建可滚动的 Frame
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f7fa")

        # 让 scrollable_frame 填满 Canvas 的宽度
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 将 scrollable_frame 添加到 Canvas 中并设置宽度绑定
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 配置 Canvas 和 Scrollbar 的布局
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 在 Canvas 宽度变化时动态更新任务框宽度
        self.canvas.bind("<Configure>", self.update_scrollable_frame_width)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # 显示任务列表
        self.display_tasks()

    def display_tasks(self):
        for task in self.tasks:
            task_frame = tk.Frame(
                self.scrollable_frame,
                bg="#ffffff",
                relief="flat",  # 去除传统的实心边框，采用扁平化设计
                bd=0,
                highlightbackground="#dddddd",  # 边框颜色为灰色
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

            # 任务的开始和截止时间
            start_time = task['start_date'].strftime("%Y-%m-%d %H:%M")
            end_time = task['end_date'].strftime("%Y-%m-%d %H:%M")
            time_frame = tk.Frame(task_frame, bg="#ffffff")
            time_frame.pack(anchor="w", pady=5)

            # 起始时间标签
            tk.Label(
                time_frame,
                text=f"Start: {start_time}",
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#555"
            ).pack(side="left", padx=(0, 10))

            # 终止时间标签，用更显眼的红色
            tk.Label(
                time_frame,
                text=f"End: {end_time}",
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#e74c3c"  # 更显眼的红色
            ).pack(side="left")

            # 显示标签
            self.show_tags(task_frame, task['tags'])

            # 完成任务按钮
            complete_button = tk.Button(
                task_frame,
                text="✔ Mark as Done",
                command=lambda t=task: self.complete_task_callback(t),
                bg="#0984e3",  # 使用现代蓝色
                fg="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=10,
                pady=5,
                activebackground="#3498db",  # 按钮悬停效果
                activeforeground="white",
                borderwidth=0
            )
            complete_button.pack(side="right", padx=10, pady=5)

    def show_tags(self, parent, tags):
        """为任务显示标签"""
        tag_colors = {"Study": "#ff9999", "Work": "#99ccff", "Private": "#99ff99"}
        tag_frame = tk.Frame(parent, bg="#ffffff")
        tag_frame.pack(anchor="w", pady=5)

        for tag in tags:
            color = tag_colors.get(tag, "#cccccc")  # 默认颜色为灰色
            tag_label = tk.Label(
                tag_frame,
                text=tag,
                bg=color,
                font=("Segoe UI", 10, "bold"),
                fg="#ffffff",
                padx=8,
                pady=3,
                relief="flat",  # 去除边框，采用扁平化设计
                bd=0
            )
            tag_label.pack(side="left", padx=5)

    def complete_task(self, task):
        """任务完成后，更新任务状态并刷新页面"""
        # 执行任务完成逻辑（可以是移除任务或标记任务完成）
        self.tasks.remove(task)  # 从任务列表中删除已完成任务
        # 在这里可以执行任务保存操作，例如调用save_tasks(self.tasks)

        # 刷新视图
        self.display_tasks()

    def update_scrollable_frame_width(self, event):
        """更新 scrollable_frame 的宽度以适应 Canvas 宽度"""
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw"),
                               width=event.width)

    def on_mouse_wheel(self, event):
        """处理鼠标滚轮事件，调整 Canvas 的垂直位置"""
        if self.canvas.winfo_exists():  # 检查 Canvas 是否有效
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
