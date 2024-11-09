class Tag:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def display(self):
        return f"Tag ID: {self.id}, Name: {self.name}"
