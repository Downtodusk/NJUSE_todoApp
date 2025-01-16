from tkinter import Frame, Button
from tkcalendar import DateEntry
from datetime import datetime

class CustomDateEntry(Frame):
    """自定义 DateEntry，支持初始为空，并可手动清空"""

    def __init__(self, parent,  **kwargs):
        super().__init__(parent)

        # 创建 DateEntry 控件
        self.date_entry = DateEntry(self, **kwargs)
        self.date_entry.pack(side="left", fill="x", expand=True)

        # 添加清除按钮
        self.clear_button = Button(self, text="X", command=self.clear_date, padx=5, pady=1)
        self.clear_button.pack(side="right")

        # 清空初始显示
        self._is_cleared = True  # 标志当前状态是否被清空
        self.clear_date()

        # 绑定事件：当用户选择日期时，更新清空标志
        self.date_entry.bind("<<DateEntrySelected>>", self._on_date_selected)

    def clear_date(self):
        """清空日期框显示"""
        self.date_entry.delete(0, "end")
        self._is_cleared = True  # 标志已清空

    def _on_date_selected(self, event):
        """当用户选择日期时，更新标志"""
        self._is_cleared = False

    def get_date(self):
        """获取日期，如果为空则返回 None，否则返回 datetime.date 对象"""
        if self._is_cleared:  # 检查是否被清空
            return None

        date_value = self.date_entry.get()
        # print(date_value)
        if not date_value:  # 未选择日期
            return None
        return datetime.strptime(date_value, "%m/%d/%y").date()
