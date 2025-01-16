from hypothesis import given, strategies as st, assume
from src.models.task import Task  # 导入你的 Task 类
from src.utils.enums import Priority  # 假设 Priority 类在 enums.py 中
from datetime import datetime, time

def date_only_strategy():
    return st.dates(min_value=datetime.now().date(), max_value=datetime(2100, 12, 31).date()).map(
        lambda d: datetime.combine(d, time(0, 0, 0))
    )

# Hypothesis 测试任务创建的输入策略
@given(
    task_id=st.integers(min_value=0, max_value=1000),
    title=st.text(min_size=0, max_size=50),
    description=st.text(min_size=0, max_size=200),
    # start_date=st.datetimes(min_value=datetime.now(), max_value=datetime(2100, 12, 31)),
    # end_date=st.datetimes(min_value=datetime.now(), max_value=datetime(2100, 12, 31)),
    start_date=date_only_strategy(),
    end_date=date_only_strategy(),
    priority=st.sampled_from(list(Priority)),
    tags=st.lists(st.text(min_size=1, max_size=20), max_size=5),
)
def test_task_creation(task_id, title, description, start_date, end_date, priority, tags):
    # assume(start_date <= end_date)

    # 创建任务对象
    task = Task(
        id=task_id,
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        priority=priority,
        tags=tags,
        reminder_time=None,
        reminder_repeats=0
    )

    # 验证任务的属性是否正确
    assert isinstance(task, Task)
    assert task.title == title
    assert task.description == description
    assert task.start_date == start_date
    assert task.end_date == end_date
    assert start_date <= end_date
    assert task.priority == priority
    assert isinstance(task.priority, Priority)
    assert isinstance(task.start_date, datetime)
    assert isinstance(task.end_date, datetime)


# 执行测试
if __name__ == "__main__":
    test_task_creation()
