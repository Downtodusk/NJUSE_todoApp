from models.tag_type import TagType

class Tag:
    def __init__(self, id, name, tag_type):
        self.id = id
        self.name = name
        self.tag_type = tag_type

    def create_tag(self):
        # 创建标签的逻辑
        pass

    def delete_tag(self):
        # 删除标签的逻辑
        pass
