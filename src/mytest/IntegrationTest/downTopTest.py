import unittest
import tkinter as tk
from tkinter import Tk
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.data.task_storage import load_tasks, save_tasks
from src.views.today_tasks_view import TodayTasksView
from src.views.all_tasks_view import AllTasksView
from src.views.timeline_view import TimelineView
import os

class TaskStorageTests(unittest.TestCase):
    def setUp(self):
        self.username = "test_user"
        self.task_file_path = f"data/{self.username}/tasks.json"
        os.makedirs(os.path.dirname(self.task_file_path), exist_ok=True)

    def test_save_and_load_tasks(self):
        tasks = [
            {
                "title": "Test Task",
                "description": "Test task description",
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(hours=1),
                "priority": "High",
                "tags": ["Work"],
                "reminder_time": None,
                "reminder_repeats": 0
            }
        ]
        save_tasks(self.username, tasks)
        loaded_tasks = load_tasks(self.username)

        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0]["title"], "Test Task")

    def tearDown(self):
        if os.path.exists(self.task_file_path):
            os.remove(self.task_file_path)


class TodayTasksViewTests(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.tasks = [
            {"title": "Today Task 1", "description": "Test Task 1", "start_date": datetime.now(),
             "end_date": datetime.now() + timedelta(days=1), "tags": ["Work"], "reminder_time": None,
             "reminder_repeats": 0},
            {"title": "Future Task", "description": "Test Future Task",
             "start_date": datetime.now() + timedelta(days=2), "end_date": datetime.now() + timedelta(days=3),
             "tags": ["Study"], "reminder_time": None, "reminder_repeats": 0},
        ]
        self.complete_task_callback = MagicMock()
        self.view = TodayTasksView(self.root, self.tasks, self.complete_task_callback)

    def test_display_today_tasks(self):
        """测试显示今天的任务"""
        self.view.display_today_tasks()  # 手动触发显示任务
        today_tasks = [task for task in self.tasks if task['start_date'].date() == datetime.now().date()]

        # 验证显示的任务数是否正确
        self.assertEqual(len(today_tasks), 1)

    def test_complete_task(self):
        """测试完成任务按钮"""
        task = self.tasks[0]
        self.view.complete_task(task)
        self.complete_task_callback.assert_called_once_with(task)

    def tearDown(self):
        self.root.destroy()


class AllTasksViewTests(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.tasks = [
            {
                "title": "Work Task",
                "description": "A task for work",
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(hours=3),
                "priority": "Low",
                "tags": ["Work"],
                "reminder_time": None,
                "reminder_repeats": 0
            },
            {
                "title": "Home Task",
                "description": "A task for home",
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(hours=5),
                "priority": "Normal",
                "tags": ["Home"],
                "reminder_time": None,
                "reminder_repeats": 0
            }
        ]

    def test_filter_tasks_by_tag(self):
        all_tasks_view = AllTasksView(self.root, self.tasks, complete_task_callback=MagicMock())

        # Simulate filtering tasks by tag "Work"
        filtered_tasks = [task for task in self.tasks if "Work" in task['tags']]
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0]['title'], "Work Task")


class TimelineViewTests(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.tasks = [
            {
                "title": "Ongoing Task",
                "description": "Currently ongoing task",
                "start_date": datetime.now() - timedelta(hours=1),
                "end_date": datetime.now() + timedelta(hours=1),
                "priority": "High",
                "tags": ["Critical"],
                "reminder_time": None,
                "reminder_repeats": 0
            }
        ]

    def test_progress_bar_calculation(self):
        timeline = TimelineView(self.root, self.tasks, complete_task_callback=MagicMock())

        now = datetime.now()
        start_time = self.tasks[0]['start_date']
        end_time = self.tasks[0]['end_date']
        total_duration = (end_time - start_time).total_seconds()
        elapsed_duration = (now - start_time).total_seconds()
        progress = min(max(elapsed_duration / total_duration, 0), 1)

        self.assertGreaterEqual(progress, 0)
        self.assertLessEqual(progress, 1)

class MainViewTests(unittest.TestCase):
    def setUp(self):
        self.username = "test_user"
        self.root = Tk()
        self.tasks = [
            {"title": "Today Task", "description": "A task for today", "start_date": datetime.now(), "end_date": datetime.now() + timedelta(hours=1), "tags": ["Work"], "reminder_time": None, "reminder_repeats": 0},
            {"title": "Future Task", "description": "A task for future", "start_date": datetime.now() + timedelta(days=1), "end_date": datetime.now() + timedelta(days=1, hours=2), "tags": ["Study"], "reminder_time": None, "reminder_repeats": 0}
        ]

    def test_switch_between_views(self):
        # Simulate the switch between views in the main app (Today, All Tasks, Timeline)
        main_view = MagicMock()
        main_view.show_today_tasks()
        main_view.show_all_tasks()
        main_view.show_timeline()

        main_view.show_today_tasks.assert_called_once()
        main_view.show_all_tasks.assert_called_once()
        main_view.show_timeline.assert_called_once()

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
