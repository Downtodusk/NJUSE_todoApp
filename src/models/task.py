from datetime import date
from src.utils.enums import Priority, Status

class Task:
    def __init__(self, id, title, description, start_date, end_date, priority=Priority.MEDIUM, tags=None, reminder_time=None, reminder_repeats=None):
        self.id = id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.priority = priority
        self.tags = tags or []
        self.reminder_time = reminder_time
        self.reminder_repeats = reminder_repeats


    def update_task(self, title=None, description=None, start_date=None, end_date=None, priority=None, reminder_time=None, reminder_repeats=None):
        self.title = title or self.title
        self.description = description or self.description
        self.start_date = start_date or self.start_date
        self.end_date = end_date or self.end_date
        self.priority = priority or self.priority
        self.reminder_time = reminder_time
        self.reminder_repeats = reminder_repeats

