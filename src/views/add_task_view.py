import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class AddTaskView(tk.Toplevel):
    def __init__(self, parent, add_task_callback):
        super().__init__(parent)
        self.add_task_callback = add_task_callback
        self.selected_tags = []  # 存储已选中的 Tag

        self.title("Add New Task")
        self.geometry("580x600")
        self.configure(bg="#f8f9fa")

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # 计算 AddTaskView 窗口的位置，使其居中于父窗口
        x = parent_x + (parent_width // 2) - (580 // 2)  # 400为窗口宽度
        y = parent_y + (parent_height // 2) - (600 // 2)  # 550为窗口高度

        # 设置窗口位置
        self.geometry(f"400x550+{x}+{y}")

        # 设置字体
        label_font = ("Segoe UI", 10, "bold")
        entry_font = ("Segoe UI", 10)

        # 标题输入框
        self.create_label("Task Title:", 0, label_font)
        self.title_entry = self.create_entry(0, entry_font)

        # 描述输入框
        self.create_label("Description:", 1, label_font)
        self.description_entry = tk.Text(self, height=4, width=40, font=entry_font, bd=1, relief="solid",
                                         highlightbackground="#ced4da", highlightthickness=1, wrap="word")
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        # 日期和时间选择框
        self.start_date = self.create_datepicker("Start Date:", 2, entry_font, label_font)
        self.end_date = self.create_datepicker("End Date:", 3, entry_font, label_font)

        self.create_priority_selector(4, label_font)

        # 标签选择框
        tk.Label(self, text="Select Tags:", bg="#f8f9fa", font=label_font).grid(row=5, column=0, sticky="w", padx=10, pady=(10, 0))
        self.tag_frame = tk.Frame(self, bg="#f8f9fa")
        self.tag_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # 可选的标签按钮
        self.available_tags = ["Study", "Work", "Private"]
        for tag in self.available_tags:
            tag_button = tk.Button(self.tag_frame, text=tag, command=lambda t=tag: self.add_tag(t), relief="flat", padx=5, pady=3, bg="#d1ecf1", font=("Segoe UI", 9))
            tag_button.grid(row=0, column=self.available_tags.index(tag), padx=5, pady=5)

        self.custom_tag_entry = tk.Entry(self.tag_frame, width=10, font=("Segoe UI", 9), relief="solid", bd=1)
        self.custom_tag_entry.grid(row=0, column=len(self.available_tags), padx=5)
        self.custom_tag_button = tk.Button(self.tag_frame, text="Add", command=self.add_custom_tag, relief="flat",
                                           padx=5, bg="#6c757d", fg="white", font=("Segoe UI", 9))
        self.custom_tag_button.grid(row=0, column=len(self.available_tags) + 1, padx=5)

        # 已选标签显示
        self.selected_tags_frame = tk.Frame(self, bg="#f8f9fa")
        self.selected_tags_frame.grid(row=6, column=1, padx=10, pady=(10, 5), sticky="w")

        # 提醒时间选择框：年-月-日 时:分:秒
        tk.Label(self, text="Reminder Time:", bg="#f8f9fa", font=label_font).grid(row=7, column=0, sticky="w", padx=10,

                                                                                  pady=(10, 0))
        # 提醒时间选择框
        self.reminder_date = self.create_datepicker("Reminder Time:", 7, entry_font, label_font)
        self.time_frame = tk.Frame(self, bg="#f8f9fa")
        self.time_frame.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.add_timepicker(self.time_frame)

        # 提醒重复次数输入框
        self.create_label("Reminder Repeats:", 9, label_font)
        self.reminder_repeats_spinbox = tk.Spinbox(self, from_=0, to=10, width=5, font=entry_font)
        self.reminder_repeats_spinbox.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # 提交和取消按钮
        self.buttons_frame = tk.Frame(self, bg="#f8f9fa")
        self.buttons_frame.grid(row=10, column=0, columnspan=2, pady=20)

        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.cancel_task, bg="#dc3545", fg="white", font=label_font, relief="flat", width=10)
        self.cancel_button.grid(row=0,column=1, padx=10, pady=5)

        self.submit_button = tk.Button(self.buttons_frame, text="Confirm", command=self.submit_task, bg="#28a745", fg="white", font=label_font, relief="flat", width=10)
        self.submit_button.grid(row=0, column=0, padx=10, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.adjust_window_size()

    def create_label(self, text, row, font):
        tk.Label(self, text=text, bg="#f8f9fa", font=font).grid(row=row, column=0, sticky="w", padx=10, pady=(10, 5))

    def create_entry(self, row, font):
        entry = tk.Entry(self, width=40, font=font, bd=1, relief="solid", highlightbackground="#ced4da",
                         highlightthickness=1)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def create_datepicker(self, text, row, entry_font, label_font):
        self.create_label(text, row, label_font)
        date_entry = DateEntry(self, width=38, font=entry_font, background="darkblue", foreground="white",
                               borderwidth=1)
        date_entry.grid(row=row, column=1, padx=10, pady=5)
        return date_entry

    def create_priority_selector(self, row, label_font):
        # 优先级标签
        tk.Label(self, text="Priority:", bg="#f8f9fa", font=label_font).grid(row=row, column=0, sticky="w", padx=10,
                                                                             pady=(10, 5))

        # 优先级变量
        self.priority_var = tk.StringVar(value="Normal")  # 默认值为 Normal

        # 优先级选择框
        priority_frame = tk.Frame(self, bg="#f8f9fa")
        priority_frame.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # 样式参数
        button_styles = {
            "Low": {
                "text": "Low",
                "bg": "#f0f0f0",  # 未选中时背景
                "activecolor": "#B8E974",  # 选中后绿色
                "hovercolor": "#e0f7dc",  # 悬停时浅绿色
                "fg": "#555555",  # 默认文字颜色
                "font": ("Segoe UI", 11)
            },
            "Normal": {
                "text": "Normal",
                "bg": "#f0f0f0",
                "activecolor": "#FFDE59",  # 选中后黄色
                "hovercolor": "#fff4cc",  # 悬停时浅黄色
                "fg": "#555555",
                "font": ("Segoe UI", 11, "bold")
            },
            "High": {
                "text": "High",
                "bg": "#f0f0f0",
                "activecolor": "#F77874",  # 选中后红色
                "hovercolor": "#fcdede",  # 悬停时浅红色
                "fg": "#555555",
                "font": ("Segoe UI", 11, "bold")
            }
        }

        # 创建按钮
        for idx, (value, style) in enumerate(button_styles.items()):
            button = tk.Radiobutton(
                priority_frame,
                text=style["text"],
                variable=self.priority_var,
                value=value,
                bg=style["bg"],
                indicatoron=0,  # 去掉默认单选按钮
                width=8,
                font=style["font"],
                selectcolor=style["activecolor"],  # 选中时的颜色
                fg=style["fg"],
                relief="flat",  # 扁平化边框
                bd=0,
                pady=8
            )
            button.grid(row=0, column=idx, padx=5)

            # 添加悬停效果
            button.bind("<Enter>", lambda e, btn=button, color=style["hovercolor"]: btn.config(bg=color))
            button.bind("<Leave>", lambda e, btn=button, color=style["bg"]: btn.config(bg=color))

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

    def add_custom_tag(self):
        """从输入框中获取自定义标签并添加到已选标签列表"""
        custom_tag = self.custom_tag_entry.get().strip()
        if custom_tag:
            self.add_tag(custom_tag)
            self.custom_tag_entry.delete(0, tk.END)  # 清空输入框

    def update_selected_tags_display(self):
        """更新已选标签的显示"""
        for widget in self.selected_tags_frame.winfo_children():
            widget.destroy()  # 删除旧的标签按钮

        # 显示所有已选标签
        for tag in self.selected_tags:
            tag_label = tk.Label(self.selected_tags_frame, text=tag, bg="#007bff", fg="white", padx=5, pady=2, relief="solid", font=("Segoe UI", 9))
            tag_label.pack(side="left", padx=5, pady=5)
            tag_label.bind("<Button-1>", lambda event, t=tag: self.remove_tag(t))

    def add_timepicker(self, frame):
        self.hours = ttk.Combobox(frame, values=[f"{i:02}" for i in range(24)], width=5, state="readonly")
        self.hours.set("00")
        self.hours.grid(row=0, column=0, padx=2)
        self.minutes = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=5, state="readonly")
        self.minutes.set("00")
        self.minutes.grid(row=0, column=1, padx=2)
        self.seconds = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=5, state="readonly")
        self.seconds.set("00")
        self.seconds.grid(row=0, column=2, padx=2)
        self.no_reminder_var = tk.BooleanVar(value=False)
        self.no_reminder_checkbox = tk.Checkbutton(frame, text="No", variable=self.no_reminder_var, bg="#f8f9fa")
        self.no_reminder_checkbox.grid(row=0, column=3, padx=10)

    def adjust_window_size(self):
        self.update_idletasks()  # 确保布局信息刷新
        required_width = self.winfo_reqwidth()
        required_height = self.winfo_reqheight()
        self.geometry(f"{required_width}x{required_height}")  # 动态设置

    def submit_task(self):
        """提交任务，验证并调用回调"""
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", "end-1c")
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        priority = self.priority_var.get()

        if self.no_reminder_var.get():  # 如果选择了“不需要提醒”
            reminder_time = None
        else:
            # 获取日期和时间部分
            reminder_date = self.reminder_date.get_date()
            reminder_hour = int(self.hours.get())
            reminder_minute = int(self.minutes.get())
            reminder_second = int(self.seconds.get())

            # 将日期和时间合并为一个datetime对象
            reminder_time = datetime(reminder_date.year, reminder_date.month, reminder_date.day,
                                     reminder_hour, reminder_minute, reminder_second)

            # 获取提醒重复次数
        reminder_repeats = int(self.reminder_repeats_spinbox.get())

        start_date_dt = datetime.combine(start_date, datetime.min.time())  # 将 datetime.date 转换为 datetime 对象
        end_date_dt = datetime.combine(end_date, datetime.min.time())  # 将 datetime.date 转换为 datetime 对象

        if not title or not description or not start_date or not end_date:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        task = {
            "title": title,
            "description": description,
            "start_date": start_date_dt,
            "end_date": end_date_dt,
            "priority": priority,
            "tags": self.selected_tags,
            "reminder_time": reminder_time,
            "reminder_repeats": reminder_repeats
        }

        self.add_task_callback(task)
        self.destroy()

    def cancel_task(self):
        if self.add_task_callback:
            self.add_task_callback(None)
        self.destroy()
