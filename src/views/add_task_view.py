import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # 导入 DateEntry

class AddTaskView(tk.Toplevel):
    def __init__(self, parent, add_task_callback):
        super().__init__(parent)
        self.add_task_callback = add_task_callback
        self.selected_tags = []  # 存储已选中的 Tag

        self.title("Add New Task")
        self.geometry("400x500")
        self.configure(bg="#f7f7f7")

        # 标题输入框
        tk.Label(self, text="Task Title:", bg="#f7f7f7").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.title_entry = tk.Entry(self, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # 描述输入框
        tk.Label(self, text="Description:", bg="#f7f7f7").grid(row=1, column=0, sticky="w", padx=10, pady=(10, 0))
        self.description_entry = tk.Text(self, height=4, width=30)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        # 日期和时间选择框，使用 DateEntry
        tk.Label(self, text="Start Date:", bg="#f7f7f7").grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.start_date = DateEntry(self, width=30, background="darkblue", foreground="white", borderwidth=2)
        self.start_date.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="End Date:", bg="#f7f7f7").grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))
        self.end_date = DateEntry(self, width=30, background="darkblue", foreground="white", borderwidth=2)
        self.end_date.grid(row=3, column=1, padx=10, pady=5)

        # 优先级选择框
        tk.Label(self, text="Priority:", bg="#f7f7f7").grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
        self.priority_var = tk.StringVar(value="Normal")
        self.priority_menu = tk.OptionMenu(self, self.priority_var, "High", "Normal", "Low")
        self.priority_menu.grid(row=4, column=1, padx=10, pady=5)

        # 标签选择框
        tk.Label(self, text="Select Tags:", bg="#f7f7f7").grid(row=5, column=0, sticky="w", padx=10, pady=(10, 0))
        self.tag_frame = tk.Frame(self, bg="#f7f7f7")
        self.tag_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # 可选的标签按钮
        self.available_tags = ["Study", "Work", "Private"]
        for tag in self.available_tags:
            tag_button = tk.Button(self.tag_frame, text=tag, command=lambda t=tag: self.add_tag(t), relief="solid", padx=5, pady=3)
            tag_button.grid(row=0, column=self.available_tags.index(tag), padx=5, pady=5)

        # 显示已选标签
        self.selected_tags_frame = tk.Frame(self, bg="#f7f7f7")
        self.selected_tags_frame.grid(row=6, column=1, padx=10, pady=(10, 5), sticky="w")

        # 提交和取消按钮
        self.buttons_frame = tk.Frame(self, bg="#f7f7f7")
        self.buttons_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.cancel_task, bg="#f44336", fg="white")
        self.cancel_button.grid(row=0, column=0, padx=10, pady=5)

        self.submit_button = tk.Button(self.buttons_frame, text="Add Task", command=self.submit_task, bg="#4CAF50", fg="white")
        self.submit_button.grid(row=0, column=1, padx=10, pady=5)

        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def add_tag(self, tag):
        """添加标签到已选标签列表"""
        if tag not in self.selected_tags:
            self.selected_tags.append(tag)
            self.update_selected_tags_display()

    def remove_tag(self, tag):
        """从已选标签中删除标签"""
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
            self.update_selected_tags_display()

    def update_selected_tags_display(self):
        """更新已选标签的显示"""
        for widget in self.selected_tags_frame.winfo_children():
            widget.destroy()  # 删除旧的标签按钮

        # 显示所有已选标签
        for tag in self.selected_tags:
            tag_label = tk.Label(self.selected_tags_frame, text=tag, bg="#2196F3", fg="white", padx=10, pady=5, relief="solid", bd=2)
            tag_label.pack(side="left", padx=5, pady=5)
            # 点击标签来删除它
            tag_label.bind("<Button-1>", lambda event, t=tag: self.remove_tag(t))

    def submit_task(self):
        """提交任务，验证并调用回调"""
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", "end-1c")
        start_date = self.start_date.get_date()  # 获取选择的开始日期
        end_date = self.end_date.get_date()  # 获取选择的结束日期
        priority = self.priority_var.get()

        if not title or not description or not start_date or not end_date:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # 创建任务字典
        task = {
            "title": title,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "priority": priority,
            "tags": self.selected_tags
        }

        # 调用回调函数传递任务数据
        self.add_task_callback(task)
        self.destroy()  # 关闭窗口

    def cancel_task(self):
        """取消任务创建"""
        self.destroy()  # 关闭窗口
