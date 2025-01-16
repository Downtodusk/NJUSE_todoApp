import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from tkinter import Tk
from src.views.add_task_view import AddTaskView


class TestAddTaskView(unittest.TestCase):

    def setUp(self):
        """为每个测试方法创建一个新的 AddTaskView 实例"""
        self.root = Tk()
        self.add_task_callback = MagicMock()  # 使用 MagicMock 作为回调
        self.view = AddTaskView(self.root, self.add_task_callback)

    def test_add_tag(self):
        """测试添加标签功能"""
        initial_tags = len(self.view.selected_tags)
        self.view.add_tag("Work")
        self.assertEqual(len(self.view.selected_tags), initial_tags + 1)
        self.assertIn("Work", self.view.selected_tags)

        # 再次添加同样的标签，不应重复
        self.view.add_tag("Work")
        self.assertEqual(len(self.view.selected_tags), initial_tags + 1)

    def test_remove_tag(self):
        """测试移除标签功能"""
        self.view.add_tag("Study")
        self.view.remove_tag("Study")
        self.assertNotIn("Study", self.view.selected_tags)

    def test_add_custom_tag(self):
        """测试添加自定义标签"""
        self.view.custom_tag_entry.insert(0, "CustomTag")
        self.view.add_custom_tag()
        self.assertIn("CustomTag", self.view.selected_tags)
        self.assertEqual(self.view.custom_tag_entry.get(), "")  # 输入框应被清空

    def test_submit_task_with_valid_data(self):
        """测试提交有效任务"""
        self.view.title_entry.insert(0, "Test Task")
        self.view.description_entry.insert("1.0", "This is a test description")
        self.view.start_date.set_date(datetime(2024, 1, 1).date())  # 修正为 datetime.date 对象
        self.view.end_date.set_date(datetime(2024, 1, 10).date())  # 修正为 datetime.date 对象
        self.view.reminder_date.set_date(datetime(2024, 1, 5).date())  # 修正为 datetime.date 对象
        self.view.priority_var.set("High")
        self.view.hours.set("10")
        self.view.minutes.set("30")
        self.view.seconds.set("00")
        self.view.reminder_repeats_spinbox.delete(0, "end")
        self.view.reminder_repeats_spinbox.insert(0, "2")

        self.view.submit_task()

        # 验证回调被调用
        self.add_task_callback.assert_called_once()
        task = self.add_task_callback.call_args[0][0]
        self.assertEqual(task["title"], "Test Task")
        self.assertEqual(task["priority"], "High")
        self.assertEqual(task["reminder_time"], datetime(2024, 1, 5, 10, 30, 0))

    def test_submit_task_with_missing_data(self):
        """测试提交不完整任务"""
        self.view.title_entry.insert(0, "Test Task")
        self.view.description_entry.insert("1.0", "This is a test description")
        self.view.start_date.set_date(datetime(2024, 1, 1).date())
        # self.view.end_date.set_date(datetime(2024, 1, 10).date())  # 缺少end_date
        self.view.reminder_date.set_date(datetime(2024, 1, 5).date())
        self.view.priority_var.set("High")

        with patch("tkinter.messagebox.showwarning") as mock_warning:
            self.view.submit_task()
            mock_warning.assert_called_once_with("Input Error", "Please fill in all fields.")

        self.add_task_callback.assert_not_called()

    def test_submit_task_without_tags(self):
        """测试没有选择标签的情况下提交任务"""
        # 填写完整的任务信息
        self.view.title_entry.insert(0, "Task Without Tags")
        self.view.description_entry.insert("1.0", "This task does not have any tags")
        self.view.start_date.set_date(datetime(2024, 1, 1).date())
        self.view.end_date.set_date(datetime(2024, 1, 10).date())
        self.view.priority_var.set("Normal")

        self.view.selected_tags = []

        self.view.submit_task()

        self.add_task_callback.assert_called_once()
        task = self.add_task_callback.call_args[0][0]

        self.assertEqual(task["title"], "Task Without Tags")
        self.assertEqual(task["description"], "This task does not have any tags")
        self.assertEqual(task["tags"], [])  # 验证没有标签

    def test_cancel_task(self):
        """测试取消任务"""
        self.view.cancel_task()
        self.add_task_callback.assert_called_once_with(None)

    def test_no_reminder(self):
        """测试不需要提醒的选项"""
        self.view.title_entry.insert(0, "No Reminder Task")
        self.view.description_entry.insert("1.0", "This is a task with no reminder")
        self.view.priority_var.set("Low")
        self.view.no_reminder_var.set(True)
        # 提交任务
        self.view.submit_task()
        # 验证回调被正确调用
        self.add_task_callback.assert_called_once()
        task = self.add_task_callback.call_args[0][0]
        self.assertIsNone(task["reminder_time"])  # 验证没有提醒时间
        self.assertEqual(task["reminder_repeats"], 0)

    def test_time_picker(self):
        """测试时间选择器功能"""
        self.view.hours.set("12")
        self.view.minutes.set("15")
        self.view.seconds.set("45")

        self.assertEqual(self.view.hours.get(), "12")
        self.assertEqual(self.view.minutes.get(), "15")
        self.assertEqual(self.view.seconds.get(), "45")

    def test_adjust_window_size(self):
        """测试窗口大小调整"""
        with patch.object(self.view, "update_idletasks") as mock_update:
            self.view.adjust_window_size()
            mock_update.assert_called_once()

    def tearDown(self):
        """清理工作"""
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
