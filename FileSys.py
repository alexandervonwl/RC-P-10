from CoAPMessage import *

class FSComponent:
    def __init__(self, name, parent, current_path='root'):
        self.name = name
        self.parent = parent
        self.current_path = current_path


class Directory(FSComponent):
    def __init__(self, name, parent):
        super().__init__(name, parent)
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

    def create_encoding(self):
        result = 'd/' + self.name + '/' + '\x00'
        if len(self.children) > 0:
            for child in self.children:
                result += child.create_encoding()
        return result


class File(FSComponent):
    def __init__(self, name, parent, content=""):
        super().__init__(name, parent)
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

    def save_into_file(self, content):
        self.content = content


class DecodePayload:
    def __init__(self, current_obj, payload):
        self.current_obj = current_obj
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
        if self.current_obj.current_path == 'root':
            return '', 405, 4
        else:
            break_path = self.current_obj.current_path.split("/")
            self.current_obj.current_path = break_path[0]
            for i in range(1, len(break_path)):
                self.current_obj.current_path += '/' + break_path[i]
            return self.current_obj.parent.create_encoding(), 204, 2

    def open(self, name):
        for child in self.current_obj.children:
            if child.name == name and child.get_type == '[DIRECTORY]':
                self.current_obj.current_path += '/' + child.name
                return child.create_encoding, 203, 2

            elif child.name == name and child.get_type == '[FILE]':
                self.current_obj.current_path += '/' + child.name
                return child.view_content, 203, 2

        return '', 404, 4

    def save(self, name):
        name_content = name.split("\x00")
        # self.save_into_file = name_content[1]
        if self.current_obj.get_type() == "[FILE]":
            if name_content[0] == name:
                self.current_obj.save_into_file(name_content[1])
                return '', 204, 2
            return '', 404, 4
        return '', 405, 4

    def new_file(self, name):
        if self.current_obj.get_type() == "[DIRECTORY]":
            self.current_obj.add_child(File(name, self))
            return '', 201, 2
        return '', 405, 4

    def new_directory(self, name):
        if self.current_obj.get_type() == "[DIRECTORY]":
            self.current_obj.add_child(Directory(name, self))
            return '', 201, 2
        return '', 405, 4

    def delete(self, name):
        for child in self.current_obj.children:
            if child.name == name:
                if child.get_type() == "[DIRECTORY]":
                    if len(child.children) == 0:
                        del child
                    else:
                        for grandchild in child.children:
                            grandchild.delete(grandchild.name)
                elif child.get_type() == "[FILE]":
                    del child
                return '', 202, 2
        return '', 404, 4
