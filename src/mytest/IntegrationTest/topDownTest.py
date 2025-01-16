import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from datetime import datetime, timedelta
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.data.task_storage import load_tasks, save_tasks
import json
import os


class TaskAppIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.username = "test_user"
        self.task_file_path = f"data/{self.username}/tasks.json"
        os.makedirs(os.path.dirname(self.task_file_path), exist_ok=True)
        with patch('src.data.task_storage.save_tasks'), patch('src.data.task_storage.load_tasks', return_value=[]):
            self.main_view = MainView(self.root, self.username)

    # ---- Login and Registration Tests ----
    @patch('src.views.login_view.LoginView.load_users')
    @patch('src.views.login_view.LoginView.save_users')
    def test_login_and_registration(self, mock_save_users, mock_load_users):
        mock_load_users.return_value = {}
        login_view = LoginView(self.root)

        # Step 1: Attempt login with incorrect credentials
        login_view.username_entry.insert(0, "new_user")
        login_view.password_entry.insert(0, "wrong_password")
        with patch("src.views.login_view.messagebox.showerror") as mock_error:
            login_view.authenticate()
            mock_error.assert_called_once_with("Login Failed", "Incorrect username or password.")

        # Step 2: Register new user
        login_view.username_entry.delete(0, "end")
        login_view.password_entry.delete(0, "end")
        login_view.username_entry.insert(0, "new_user")
        login_view.password_entry.insert(0, "new_password")
        with patch("src.views.login_view.messagebox.showinfo") as mock_info:
            login_view.register()
            mock_info.assert_called_once_with("Register Success", "Registration successful. Please login.")
            mock_save_users.assert_called_once_with({"new_user": "new_password"})

        # Step 3: Login with registered credentials
        mock_load_users.return_value = {"new_user": "new_password"}
        login_view.authenticate()
        self.assertIsInstance(self.main_view, MainView)

    # ---- Task Management Tests ----
    @patch('src.data.task_storage.save_tasks')
    def test_task_creation_and_completion(self, mock_save_tasks):
        initial_task_count = len(self.main_view.tasks)

        # Create a new task
        new_task = {
            "title": "Integration Test Task",
            "description": "Testing task creation",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=2),
            "priority": "High",
            "tags": ["Test"],
            "reminder_time": None,
            "reminder_repeats": 0
        }
        with patch.object(self.main_view, 'refresh_current_view', return_value=None):
            self.main_view.add_task(new_task)

        self.assertEqual(len(self.main_view.tasks), initial_task_count + 1)

        # Mark task as complete
        with patch.object(self.main_view, 'refresh_current_view', return_value=None):
            self.main_view.complete_task(new_task)
        self.assertEqual(len(self.main_view.tasks), initial_task_count)

    def test_task_reminders(self):
        reminder_task = {
            "title": "Reminder Task",
            "description": "Task with reminder",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=1),
            "priority": "Normal",
            "tags": [],
            "reminder_time": datetime.now(),
            "reminder_repeats": 1
        }
        self.main_view.add_task(reminder_task)

        # Simulate reminder triggering
        with patch("src.views.main_view.messagebox.showinfo") as mock_info:
            self.main_view.check_reminders()
            mock_info.assert_called_once_with("Reminder", f"Reminder for Task: {reminder_task['title']}")

    # ---- View Switching Tests ----
    def test_view_switching(self):
        self.main_view.show_today_tasks()
        self.assertEqual(self.main_view.current_view, "today")

        self.main_view.show_all_tasks()
        self.assertEqual(self.main_view.current_view, "all")

        self.main_view.show_timeline()
        self.assertEqual(self.main_view.current_view, "timeline")

    # ---- Data Storage Tests ----
    def test_data_storage(self):
        self.main_view.load_tasks_data()
        self.assertEqual(len(self.main_view.tasks), 0)

        new_task = {
            "title": "Saved Task",
            "description": "Persistent task",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=1),
            "priority": "Low",
            "tags": ["Persistent"],
            "reminder_time": None,
            "reminder_repeats": 0
        }
        self.main_view.add_task(new_task)

        # Verify that the task is saved in the JSON file
        with open(self.task_file_path, 'r') as file:
            saved_tasks = json.load(file)
            self.assertEqual(len(saved_tasks), 1)
            self.assertEqual(saved_tasks[0]['title'], "Saved Task")

    def tearDown(self):
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
