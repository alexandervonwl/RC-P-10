class FSComponent:
    def __init__(self, name, parent, level=0, current_path='d/root'):
        self.name = name
        self.parent = parent
        self.current_path = current_path
        self.level = level
        self.children = set()
        self.type = ''


class Directory(FSComponent):
    def __init__(self, name, parent, level):
        super().__init__(name, parent, level)
        self.type = '[DIRECTORY]'

    def add_child(self, child: FSComponent):
        self.children.add(child)

    def __str__(self):
        result = f"[DIRECTORY]: {self.name}"
        if len(self.children) > 0:
            result += '\n'
            for child in self.children:
                result += '\t' * child.level
                if child.type == '[FILE]':
                    result += f"L{child.type}: {child.name} {child.content} \n"
                elif child.type == '[DIRECTORY]':
                    result += 'L' + child.__str__() + '\n'
        return result

    def create_encoding(self):
        result = '\x00'
        if len(self.children) > 0:
            for child in self.children:
                if child.type == '[FILE]':
                    result += 'f' + child.name + '\x00'
                elif child.type == '[DIRECTORY]':
                    result += 'd' + child.name + '\x00'
        return result


class File(FSComponent):
    def __init__(self, name, parent, level, content=""):
        super().__init__(name, parent, level)
        self.content = content
        self.type = '[FILE]'

    def __str__(self):
        return f"[FILE]: {self.name} {self.content}"

    def create_encoding(self):
        result = 'f' + self.name
        return result

    def view_content(self):
        result = self.content + '\x00'
        return result

    def save_into_file(self, content):
        self.content = content



