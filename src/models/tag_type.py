class TagType:
    def __init__(self, type_name):
        self.type_name = type_name

    @staticmethod
    def get_predefined_types():
        return ["Personal", "Work", "Urgent"]
