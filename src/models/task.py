from datetime import date
from ..utils.enums import Priority, Status

class Task:
    def __init__(self, id, title, description, start_date, end_date, priority=Priority.MEDIUM, status=Status.TODO, tags=None):
        self.id = id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.priority = priority
        self.status = status
        self.tags = tags or []

    def create_task(self):
        # 创建任务的逻辑
        pass

    def update_task(self):
        # 更新任务的逻辑
        pass

    def delete_task(self):
        # 删除任务的逻辑
        pass

    def set_reminder(self):
        # 设置提醒的逻辑
        pass

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)
