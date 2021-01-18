class FSComponent:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.current_path = ''
        self.children = set()
class Directory(FSComponent):
    def __init__(self, name):
        super().__init__(name)

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

    def create_encoding(self):
        result = 'd/' + self.name + '/' + '\x00'
        if len(self.children) > 0:
            for child in self.children:
                result += child.create_encoding()
        return result

class File(FSComponent):
    def __init__(self, name, content):
        super().__init__(name)
        self.content = content

    def get_type(self):
        return "[FILE]"

    def __str__(self):
        return f"[FILE]: {self.name} {self.content}"

    def create_encoding(self):
        result = 'f' + self.name + '\x00'
        return result

    def view_content(self):
        result = 'f' + self.content
        return result


class DecodePayload(FSComponent):
    def __init__(self, payload, name, parent):
        super().__init__(name, parent)
        self.payload = payload
        self.command = ""
        self.name = ""

    def parsePayload(self):
        self.command = self.payload[0:4]
        self.name = self.payload[4:]

        self.execute(self.command, self.name)

    def execute(self, command, name):
        return {
            '\x01': self.command_back(name),
            '\x02': self.open(name),
            '\x03': self.save(name),
            '\x04': self.new_file(name),
            '\x05': self.new_directory(name),
            '\x06': self.delete(name),
        }[command]

    def command_back(self, name):
        return self.parent

    def open(self, name):
        for child in self.children:
            if child.name == name and child.get_type == '[Directory]':
                return child.create_encoding

            elif child.name == name and child.get_type == '[FILE]':
                return child.view_content

        return 'eroare'

    def save(self, name):
        pass

    def new_file(self, name):
        pass

    def new_directory(self, name):
        pass

    def delete(self, name):
        pass

