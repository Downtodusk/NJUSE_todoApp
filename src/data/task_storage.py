import json
import os
from datetime import datetime

# 基础路径，用户任务存储目录
BASE_DATA_PATH = "data"

def get_task_file_path(username):
    """获取用户任务文件路径"""
    return os.path.join(BASE_DATA_PATH, username, "tasks.json")

def load_tasks(username):
    """从文件加载任务数据"""
    user_task_file = get_task_file_path(username)
    try:
        with open(user_task_file, "r") as file:
            tasks_data = json.load(file)
            # 将字符串日期转换为 datetime 对象
            for task in tasks_data:
                if task["reminder_time"]:
                    task["reminder_time"] = datetime.strptime(task["reminder_time"], "%Y-%m-%d %H:%M:%S")
                if task.get("start_date"):
                    task["start_date"] = datetime.strptime(task["start_date"], "%Y-%m-%d %H:%M:%S")
                if task.get("end_date"):
                    task["end_date"] = datetime.strptime(task["end_date"], "%Y-%m-%d %H:%M:%S")
            return tasks_data
    except FileNotFoundError:
        print(f"File {user_task_file} not found. Returning empty task list.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {user_task_file}. Returning empty task list.")
        return []

def save_tasks(username, tasks):
    """保存任务到文件"""
    user_task_file = get_task_file_path(username)
    os.makedirs(os.path.dirname(user_task_file), exist_ok=True)  # 确保用户目录存在

    with open(user_task_file, "w") as file:
        tasks_data = []
        for task in tasks:
            # 将 datetime 对象转换为字符串
            task_data = task.copy()
            task_data["start_date"] = task["start_date"].strftime("%Y-%m-%d %H:%M:%S") if task["start_date"] else None
            task_data["end_date"] = task["end_date"].strftime("%Y-%m-%d %H:%M:%S") if task["end_date"] else None
            task_data["reminder_time"] = task["reminder_time"].strftime("%Y-%m-%d %H:%M:%S") if task["reminder_time"] else None
            tasks_data.append(task_data)

        json.dump(tasks_data, file, indent=4)
