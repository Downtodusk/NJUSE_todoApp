from task import Task

class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.tasks = []

    def register(self):
        # 注册逻辑
        pass

    def login(self):
        # 登录逻辑
        pass

    def logout(self):
        # 注销逻辑
        pass

    def sync_tasks(self):
        # 同步任务的逻辑
        pass
