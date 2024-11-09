from datetime import date

class Reminder:
    def __init__(self, id, task_id, reminder_time, is_recurring=False):
        self.id = id
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.is_recurring = is_recurring

    def display(self):
        return f"Reminder ID: {self.id}, Task ID: {self.task_id}, Reminder Time: {self.reminder_time}"
