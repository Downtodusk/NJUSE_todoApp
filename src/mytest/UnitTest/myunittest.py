import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from tkinter import Tk
from src.views.main_view import MainView
from src.data.task_storage import load_tasks, save_tasks
import sys
import os

# 将 src 目录加入到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'src')))


class TestMainView(unittest.TestCase):

    def setUp(self):
        """为每个测试方法创建一个新的 MainView 实例"""
        self.root = Tk()
        self.username = "test_user"
        self.view = MainView(self.root, self.username)

    def test_add_task(self):
        """测试添加任务功能"""
        task = {
            "title": "Test2",
            "description": "This is another test",
            "start_date": datetime(2024, 11, 1, 0, 0, 0),  # 使用datetime对象
            "end_date": datetime(2024, 12, 1, 0, 0, 0),  # 使用datetime对象
            "priority": "High",
            "tags": [
                "Private"
            ],
            "reminder_time": None,
            "reminder_repeats": 0
        }
        initial_task_count = len(self.view.tasks)
        self.assertEqual(initial_task_count, 1)
        print("initial task count: ", initial_task_count)
        self.view.add_task(task)  # 调用添加任务方法
        self.assertEqual(len(self.view.tasks), initial_task_count + 1)  # 确保任务数增加
        self.assertEqual(self.view.tasks[-1]["title"], "Test2")  # 确保新任务标题正确
        self.assertIsInstance(self.view.tasks[-1]["start_date"], datetime)  # 确保start_date是datetime对象
        self.assertIsInstance(self.view.tasks[-1]["end_date"], datetime)

    def test_add_task_with_invalid_data(self):
        """测试添加无效任务时的处理"""
        task = None
        initial_task_count = len(self.view.tasks)
        self.view.add_task(task)  # 传入 None 应该不增加任务
        self.assertEqual(len(self.view.tasks), initial_task_count)

    def test_complete_task(self):
        """测试完成任务功能"""
        task = self.view.tasks[-1]
        task_len = len(self.view.tasks)
        self.view.complete_task(task)
        self.assertEqual(len(self.view.tasks), task_len - 1)  # 任务数量应该减少
        self.assertNotIn(task, self.view.tasks)  # 完成的任务应该不再在任务列表中

    def test_check_reminders_with_upcoming_reminder(self):
        """测试提醒功能，任务的提醒时间即将到达"""
        task = {
            "title": "Reminder Task",
            "description": "This is a reminder test",
            "start_date": datetime(2024, 11, 1, 0, 0, 0),  # 示例起始时间
            "end_date": datetime(2024, 12, 1, 0, 0, 0),  # 示例结束时间
            "priority": "Normal",  # 示例优先级
            "tags": ["Work"],  # 示例标签
            "reminder_time": datetime.now(),  # 设置提醒时间即将到达
            "reminder_repeats": 1  # 示例提醒次数
        }
        self.view.add_task(task)

        # 使用 MagicMock 来模拟 messagebox.showinfo
        with patch("src.views.main_view.messagebox.showinfo") as mock_showinfo:
            self.view.check_reminders()
            mock_showinfo.assert_called_once_with("Reminder", f"Reminder for Task: {task['title']}")

        # 确保提醒次数正确更新
        self.assertEqual(self.view.tasks[0]["reminder_repeats"], 0)
        self.assertEqual(self.view.tasks[0]["reminder_time"], None)

    from unittest.mock import patch
    from datetime import datetime

    def test_check_reminders_no_upcoming(self):
        """测试没有任务需要提醒的情况"""
        task = {
            "title": "No Reminder",
            "description": "This task has no reminder",
            "start_date": datetime(2024, 11, 1, 0, 0, 0),
            "end_date": datetime(2024, 12, 31, 0, 0, 0),
            "priority": "Low",  # 示例优先级
            "tags": [],  # 空标签
            "reminder_time": None,  # 没有提醒时间
            "reminder_repeats": 0  # 不需要重复提醒
        }
        self.view.add_task(task)

        # 使用 MagicMock 来模拟 messagebox.showinfo
        with patch("src.views.main_view.messagebox.showinfo") as mock_showinfo:
            self.view.check_reminders()
            mock_showinfo.assert_not_called()  # 不应调用任何提醒弹窗

    def test_show_today_tasks(self):
        """测试显示今天的任务"""
        self.view.show_today_tasks()
        self.assertEqual(self.view.current_view, "today")

    def test_show_all_tasks(self):
        """测试显示所有任务"""
        self.view.show_all_tasks()
        self.assertEqual(self.view.current_view, "all")

    def test_show_timeline(self):
        """测试显示任务时间线"""
        self.view.show_timeline()
        self.assertEqual(self.view.current_view, "timeline")

    def test_refresh_current_view(self):
        """测试刷新当前视图"""
        self.view.show_all_tasks()
        self.view.refresh_current_view()
        self.assertEqual(self.view.current_view, "all")  # 视图应该保持为 "all"

    def test_clear_content(self):
        """测试清空内容区域"""
        self.view.clear_content()
        self.assertEqual(len(self.view.content.winfo_children()), 0)  # 内容区应为空

    def tearDown(self):
        """测试后清理工作"""
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
