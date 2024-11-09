from models.user import User
from models.task import Task
from views.all_tasks_view import AllTasksView
from views.timeline_view import TimelineView
from datetime import date
from utils.enums import Priority, Status

class UI:
    def __init__(self):
        self.user = User(id=1, username="testuser", email="test@example.com", password="password")

    def run(self):
        while True:
            print("\n1. View Tasks\n2. Add Task\n3. Remove Task\n4. Timeline View\n5. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.display_all_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.remove_task()
            elif choice == "4":
                self.timeline_view()
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")

    def display_all_tasks(self):
        view = AllTasksView(self.user.tasks)
        view.display_tasks()

    def add_task(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        start_date = date.today()
        end_date = date.today()  # Placeholder; real app would parse user input
        priority = Priority.MEDIUM
        status = Status.TODO
        task = Task(id=len(self.user.tasks) + 1, title=title, description=description, start_date=start_date, end_date=end_date, priority=priority, status=status)
        self.user.add_task(task)
        print("Task added.")

    def remove_task(self):
        task_id = int(input("Enter task ID to remove: "))
        self.user.remove_task(task_id)
        print("Task removed.")

    def timeline_view(self):
        view = TimelineView(self.user.tasks)
        view.display_timeline()
