class TagType:
    def __init__(self, type_name):
        self.type_name = type_name

    @staticmethod
    def get_predefined_types():
        # 返回预定义标签类型列表
        return ["Personal", "Work", "Urgent"]
