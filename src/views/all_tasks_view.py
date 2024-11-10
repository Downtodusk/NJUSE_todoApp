import tkinter as tk
from tkinter import ttk

class AllTasksView:
    def __init__(self, parent, tasks, complete_task_callback):
        self.parent = parent
        self.tasks = tasks
        self.complete_task_callback = complete_task_callback
        self.filtered_tasks = tasks  # 初始显示所有任务
        self.available_tags = self.get_unique_tags()  # 获取唯一标签列表

        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(self.parent, bg="#f5f7fa", highlightthickness=0)
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

        # 创建标签过滤器
        self.create_filter_bar()

        # 显示任务列表
        self.display_tasks()

    def get_unique_tags(self):
        """获取所有任务中的唯一标签列表"""
        tags = {"All Tasks"}
        for task in self.tasks:
            tags.update(task.get("tags", []))
        return list(tags)

    def create_filter_bar(self):
        """在界面顶部创建标签选择过滤器"""
        filter_frame = tk.Frame(self.parent, bg="#f5f7fa")
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Filter by Tag:", font=("Segoe UI", 12), bg="#f5f7fa").pack(side="left", padx=5)

        self.tag_filter = ttk.Combobox(
            filter_frame,
            values=self.available_tags,
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.tag_filter.set("All Tasks")  # 默认选择所有任务
        self.tag_filter.pack(side="left", padx=5)

        self.tag_filter.bind("<<ComboboxSelected>>", self.filter_tasks)

    def filter_tasks(self, event=None):
        """根据选中的标签过滤任务"""
        selected_tag = self.tag_filter.get()
        if selected_tag == "All Tasks":
            self.filtered_tasks = self.tasks
        else:
            self.filtered_tasks = [task for task in self.tasks if selected_tag in task.get("tags", [])]
        self.display_tasks()

    def display_tasks(self):
        """清空并显示任务列表"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for task in self.filtered_tasks:
            task_frame = tk.Frame(
                self.scrollable_frame,
                bg="#ffffff",
                relief="flat",
                bd=0,
                highlightbackground="#e0e0e0",
                highlightthickness=1,
                padx=10,
                pady=15
            )
            task_frame.pack(anchor="w", padx=10, pady=10, fill="x")

            # 添加阴影效果
            task_frame.config(highlightthickness=1, highlightcolor="#dddddd", relief="flat")

            # 任务标题和描述
            tk.Label(
                task_frame,
                text=task['title'],
                font=("Segoe UI", 14, "bold"),
                bg="#ffffff",
                fg="#333333"
            ).pack(anchor="w", pady=5)

            tk.Label(
                task_frame,
                text=task['description'],
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#666666"
            ).pack(anchor="w", pady=5)

            # 显示标签
            self.show_tags(task_frame, task['tags'])

            # 添加“完成”按钮
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
                activebackground="#1e88e5",
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
