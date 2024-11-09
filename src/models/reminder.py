from datetime import date

class Reminder:
    def __init__(self, id, task_id, reminder_time, recurring_times=0, recurring_gaps=0, is_recurring=False):
        self.id = id
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.recurring_times = recurring_times
        self.recurring_gaps = recurring_gaps
        self.is_recurring = is_recurring

    def set_reminder(self):
        # 设置提醒逻辑
        pass

    def delete_reminder(self):
        # 删除提醒逻辑
        pass

    def update_reminder(self):
        # 更新提醒逻辑
        pass
