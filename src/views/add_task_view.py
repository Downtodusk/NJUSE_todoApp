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
        self.geometry("520x600")
        self.configure(bg="#e9ecef")

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # 计算 AddTaskView 窗口的位置，使其居中于父窗口
        x = parent_x + (parent_width // 2) - (520 // 2)  # 400为窗口宽度
        y = parent_y + (parent_height // 2) - (600 // 2)  # 550为窗口高度

        # 设置窗口位置
        self.geometry(f"400x550+{x}+{y}")

        # 设置字体
        label_font = ("Arial", 10, "bold")
        entry_font = ("Arial", 10)

        # 标题输入框
        tk.Label(self, text="Task Title:", bg="#e9ecef", font=label_font).grid(row=0, column=0, sticky="w", padx=10, pady=(15, 0))
        self.title_entry = tk.Entry(self, width=35, font=entry_font, bd=1, relief="solid")
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # 描述输入框
        tk.Label(self, text="Description:", bg="#e9ecef", font=label_font).grid(row=1, column=0, sticky="w", padx=10, pady=(10, 0))
        self.description_entry = tk.Text(self, height=4, width=35, font=entry_font, bd=1, relief="solid", wrap="word")
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        # 日期和时间选择框
        tk.Label(self, text="Start Date:", bg="#e9ecef", font=label_font).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.start_date = DateEntry(self, width=33, font=entry_font, background="darkblue", foreground="white", borderwidth=1)
        self.start_date.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="End Date:", bg="#e9ecef", font=label_font).grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))
        self.end_date = DateEntry(self, width=33, font=entry_font, background="darkblue", foreground="white", borderwidth=1)
        self.end_date.grid(row=3, column=1, padx=10, pady=5)

        # 优先级选择框
        tk.Label(self, text="Priority:", bg="#e9ecef", font=label_font).grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
        self.priority_var = tk.StringVar(value="Normal")
        self.priority_menu = tk.OptionMenu(self, self.priority_var, "High", "Normal", "Low")
        self.priority_menu.config(width=32, font=entry_font)
        self.priority_menu.grid(row=4, column=1, padx=10, pady=5)

        # 标签选择框
        tk.Label(self, text="Select Tags:", bg="#e9ecef", font=label_font).grid(row=5, column=0, sticky="w", padx=10, pady=(10, 0))
        self.tag_frame = tk.Frame(self, bg="#e9ecef")
        self.tag_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # 可选的标签按钮
        self.available_tags = ["Study", "Work", "Private"]
        for tag in self.available_tags:
            tag_button = tk.Button(self.tag_frame, text=tag, command=lambda t=tag: self.add_tag(t), relief="flat", padx=5, pady=3, bg="#d1ecf1", font=("Arial", 9))
            tag_button.grid(row=0, column=self.available_tags.index(tag), padx=5, pady=5)

        # 已选标签显示
        self.selected_tags_frame = tk.Frame(self, bg="#e9ecef")
        self.selected_tags_frame.grid(row=6, column=1, padx=10, pady=(10, 5), sticky="w")

        # 提醒时间选择框：年-月-日 时:分:秒
        tk.Label(self, text="Reminder Time:", bg="#e9ecef", font=label_font).grid(row=7, column=0, sticky="w", padx=10,
                                                                                  pady=(10, 0))

        # 日期选择控件（年-月-日）
        self.reminder_date = DateEntry(self, width=33, font=entry_font, background="darkblue", foreground="white",
                                       borderwidth=1)
        self.reminder_date.grid(row=7, column=1, padx=10, pady=5)

        # 时间选择（时：分：秒）
        self.time_frame = tk.Frame(self, bg="#e9ecef")
        self.time_frame.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.hours = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(24)], width=5, state="readonly")
        self.hours.set("00")
        self.hours.grid(row=0, column=0, padx=2)

        self.minutes = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(60)], width=5, state="readonly")
        self.minutes.set("00")
        self.minutes.grid(row=0, column=1, padx=2)

        self.seconds = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(60)], width=5, state="readonly")
        self.seconds.set("00")
        self.seconds.grid(row=0, column=2, padx=2)

        # 无提醒选项
        self.no_reminder_var = tk.BooleanVar(value=False)
        self.no_reminder_checkbox = tk.Checkbutton(self.time_frame, text="No", variable=self.no_reminder_var,
                                                   bg="#e9ecef")
        self.no_reminder_checkbox.grid(row=0, column=3, padx=10)

        # 提醒重复次数输入框
        tk.Label(self, text="Reminder Repeats:", bg="#e9ecef", font=label_font).grid(row=9, column=0, sticky="w",
                                                                                     padx=10, pady=(10, 0))
        self.reminder_repeats_spinbox = tk.Spinbox(self, from_=0, to=10, width=5, font=entry_font)
        self.reminder_repeats_spinbox.grid(row=9, column=1, padx=10, pady=5, sticky="w")


        # 提交和取消按钮
        self.buttons_frame = tk.Frame(self, bg="#e9ecef")
        self.buttons_frame.grid(row=10, column=0, columnspan=2, pady=20)

        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.cancel_task, bg="#dc3545", fg="white", font=label_font, relief="flat", width=10)
        self.cancel_button.grid(row=0,column=1, padx=10, pady=5)

        self.submit_button = tk.Button(self.buttons_frame, text="Confirm", command=self.submit_task, bg="#28a745", fg="white", font=label_font, relief="flat", width=10)
        self.submit_button.grid(row=0, column=0, padx=10, pady=5)

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
            tag_label = tk.Label(self.selected_tags_frame, text=tag, bg="#007bff", fg="white", padx=5, pady=2, relief="solid", font=("Arial", 9))
            tag_label.pack(side="left", padx=5, pady=5)
            tag_label.bind("<Button-1>", lambda event, t=tag: self.remove_tag(t))

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
        self.destroy()
