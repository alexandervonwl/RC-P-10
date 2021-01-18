class FSComponent:
    def __init__(self, name, parent, current_path='root'):
        self.name = name
        self.parent = parent
        self.current_path = current_path
        self.children = set()
        self.type = ''


class Directory(FSComponent):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.type = '[DIRECTORY]'

    def add_child(self, child: FSComponent):
        self.children.add(child)

    def __str__(self):
        result = f"[DIRECTORY]: {self.name}"
        if len(self.children) > 0:
            result += "\n"
            for child in self.children:
                if child.type == '[FILE]':
                    result += f"L{child.type}{child.name} {child.content} \n"
                elif child.type == '[DIRECTORY]':
                    result += f"L{child} \n"
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
        self.type = '[FILE]'

    '''def get_type(self):
        return "[FILE]"'''

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

        return self.execute(self.command, self.name)
        # return '', 400, 4

    def execute(self, command, name):
        if command == '\\x01':
            return self.command_back(name)
        elif command == '\\x02':
            return self.open(name)
        elif command == '\\x03':
            return self.save(name)
        elif command == '\\x04':
            return self.new_file(name)
        elif command == "\\x05":
            return self.new_directory(name)
        elif command == '\\x06':
            return self.delete(name)
        else:
            return '', 400, 4

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
            if child.name == name and child.type == '[DIRECTORY]':
                self.current_obj.current_path += '/' + child.name
                return child.create_encoding, 203, 2

            elif child.name == name and child.type == '[FILE]':
                self.current_obj.current_path += '/' + child.name
                return child.view_content, 203, 2

        return '', 404, 4

    def save(self, name):
        name_content = name.split("\x00")
        # self.save_into_file = name_content[1]
        if self.current_obj.type == "[FILE]":
            if name_content[0] == name:
                self.current_obj.save_into_file(name_content[1])
                return '', 204, 2
            return '', 404, 4
        return '', 405, 4

    def new_file(self, name):
        if self.current_obj.type == "[DIRECTORY]":
            self.current_obj.add_child(File(name, self.current_obj))
            return '', 201, 2
        return '', 405, 4

    def new_directory(self, name):
        if self.current_obj.type == "[DIRECTORY]":
            self.current_obj.add_child(Directory(name, self.current_obj))
            return '', 201, 2
        return '', 405, 4

    def delete(self, name):
        for child in self.current_obj.children:
            if child.name == name:
                if child.type == "[DIRECTORY]":
                    if len(child.children) == 0:
                        del child
                    else:
                        for grandchild in child.children:
                            grandchild.delete(grandchild.name)
                elif child.type == "[FILE]":
                    del child
                return '', 202, 2
        return '', 404, 4
