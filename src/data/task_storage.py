import json
from datetime import datetime

# 存储文件路径
TASKS_FILE = "tasks.json"

def load_tasks():
    """从文件加载任务数据"""
    try:
        with open(TASKS_FILE, "r") as file:
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
        print(f"File {TASKS_FILE} not found. Returning empty task list.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {TASKS_FILE}. Returning empty task list.")
        return []



def save_tasks(tasks):
    """保存任务到文件"""
    with open(TASKS_FILE, "w") as file:
        tasks_data = []
        for task in tasks:
            # 将 datetime 对象转换为字符串
            task_data = task.copy()
            task_data["start_date"] = task["start_date"].strftime("%Y-%m-%d %H:%M:%S") if task["start_date"] else None
            task_data["end_date"] = task["end_date"].strftime("%Y-%m-%d %H:%M:%S") if task["end_date"] else None
            task_data["reminder_time"] = task["reminder_time"].strftime("%Y-%m-%d %H:%M:%S") if task[
                "reminder_time"] else None
            tasks_data.append(task_data)

        json.dump(tasks_data, file, indent=4)
