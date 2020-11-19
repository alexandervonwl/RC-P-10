class FSComponent:
    def __init__(self, name):
        self.name = name

class Directory(FSComponent):
    def __init__(self, name):
        super().__init__(name)
        self.children = set()

    def add_child(self, child: FSComponent):
        self.children.add(child)

    def get_type(self):
        return "[DIRECTORY]"

    def __str__(self):
        result = f"[DIRECTORY]: {self.name}"
        if len(self.children) > 0:
            result += "\n"
            for child in self.children:
                result += f"L{child.get_type()}{child.name} {child.content} \n"
        return result

class File(FSComponent):
    def __init__(self, name, content):
        super().__init__(name)
        self.content = content

    def get_type(self):
        return "[FILE]"

    def __str__(self):
        return f"[FILE]: {self.name} {self.content}"