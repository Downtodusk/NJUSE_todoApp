import unittest
from hypothesis import given, strategies as st
from unittest.mock import patch
from datetime import datetime, timedelta
from src.views.main_view import MainView
from tkinter import Tk

class TestReminderFunctionalityFuzz(unittest.TestCase):

    def setUp(self):
        """初始化测试环境"""
        self.root = Tk()  # 使用 Mock 取代 Tk 实例，减少 UI 依赖
        self.username = "test_user"
        self.main_view = MainView(self.root, self.username)
        self.main_view.tasks = []  # 初始化任务列表

    @given(
        reminder_time=st.one_of(
            st.none(),  # None 表示没有提醒
            st.datetimes(min_value=datetime(2000, 1, 1), max_value=datetime(2100, 12, 31))
        ),
        reminder_repeats=st.integers(min_value=0, max_value=10)  # 重复次数，包含负数和边界情况
    )
    def test_task_reminder_logic(self, reminder_time, reminder_repeats):
        """模糊测试提醒功能"""
        # 构建任务
        task = {
            "title": "Reminder Task",
            "description": "This is a test for reminders",
            "start_date": datetime.now() - timedelta(days=1),
            "end_date": datetime.now() + timedelta(days=1),
            "priority": "High",
            "tags": ["Test"],
            "reminder_time": reminder_time,
            "reminder_repeats": reminder_repeats
        }
        # if(reminder_time):
        #     assert reminder_time >= task["start_date"]

        self.main_view.tasks.clear()
        self.main_view.tasks.append(task)
        print(self.main_view.tasks)

        with patch("src.views.main_view.messagebox.showinfo") as mock_showinfo:
            self.main_view.check_reminders()

            # 逻辑验证
            if reminder_time and datetime.now() >= reminder_time:

                # 检查提醒次数是否正确更新
                if reminder_repeats > 0:
                    mock_showinfo.assert_called_once_with("Reminder", f"Reminder for Task: {task['title']}")
                    self.assertEqual(task["reminder_repeats"], reminder_repeats - 1)
                else:
                    self.assertIsNone(task["reminder_time"])  # 提醒时间应被置空
            else:
                # 未到提醒时间或无提醒时间，showinfo 不应被调用
                mock_showinfo.assert_not_called()

    def tearDown(self):
        """清理测试环境"""
        self.main_view.tasks.clear()

if __name__ == "__main__":
    unittest.main()
