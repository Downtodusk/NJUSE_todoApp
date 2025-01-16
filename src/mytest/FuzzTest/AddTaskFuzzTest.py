import unittest
from hypothesis import given, strategies as st
from tkinter import Tk
from src.views.add_task_view import AddTaskView

class TestAddTaskViewFuzz(unittest.TestCase):
    def setUp(self):
        """初始化 AddTaskView 测试环境"""
        self.root = Tk()
        self.added_tasks = []  # 存储添加的任务
        self.view = AddTaskView(self.root, self.mock_add_task_callback)

    def mock_add_task_callback(self, task):
        """模拟添加任务的回调函数"""
        if task is not None:
            self.added_tasks.append(task)

    @given(
        title=st.text(min_size=0, max_size=500),  # Title：空字符串到超长字符串
        description=st.text(min_size=0, max_size=1000)  # Description：空字符串到超长字符串
    )
    def test_task_title_and_description_input(self, title, description):
        """对任务标题和描述进行模糊测试"""
        # 插入生成的输入到界面控件中
        self.view.title_entry.delete(0, "end")
        self.view.title_entry.insert(0, title)

        self.view.description_entry.delete("1.0", "end")
        self.view.description_entry.insert("1.0", description)

        # 模拟用户点击提交按钮
        self.view.submit_task()

        # 检查任务数据是否被正确捕获
        if title and description:  # 只有当标题和描述非空时才会添加任务
            self.assertTrue(self.added_tasks)
            task = self.added_tasks[-1]
            self.assertEqual(task["title"], title)
            self.assertEqual(task["description"], description)
        else:
            # 如果输入无效（标题或描述为空），任务不应被添加
            self.assertFalse(self.added_tasks)

    def tearDown(self):
        """清理测试环境"""
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
