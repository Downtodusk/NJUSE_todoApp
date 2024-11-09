class AllTasksView:
    def __init__(self, tasks, view_type="list"):
        self.tasks = tasks
        self.view_type = view_type

    def display_tasks(self):
        # 展示任务的逻辑
        pass

    def set_view_type(self, view_type):
        self.view_type = view_type

    def add_task_to_calendar(self, task):
        # 添加任务到日历
        pass

    def remove_task_from_calendar(self, task):
        # 从日历中移除任务
        pass

    def filter_tasks_by_tag(self, tag):
        # 按标签过滤任务
        return [task for task in self.tasks if tag in task.tags]
