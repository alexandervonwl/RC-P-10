from FileSys import *


class DecodePayload:
    def __init__(self, current_obj, payload):
        self.current_obj = current_obj
        self.payload = payload
        self.command = ""
        self.name = ""

    def parsePayload(self):
        self.command = self.payload[0]
        self.name = self.payload[1:]

        return self.execute(self.command, self.name)

    def execute(self, command, name):
        if command == '\x01':
            return self.command_back()
        elif command == '\x02':
            return self.open(name)
        elif command == '\x03':
            return self.save(name)
        elif command == '\x04':
            return self.new_file(name)
        elif command == '\x05':
            return self.new_directory(name)
        elif command == '\x06':
            return self.delete(name)
        else:
            return '', 0, 4

    def command_back(self):
        if self.current_obj.current_path == 'd/root':
            return '', 5, 4
        else:
            self.current_obj = self.current_obj.parent
            return self.current_obj.current_path + self.current_obj.create_encoding(), 4, 2

    def open(self, name):
        for child in self.current_obj.children:
            if child.name == name and child.type == '[DIRECTORY]':
                path = self.current_obj.current_path
                self.current_obj = child
                path += '/' + child.name
                self.current_obj.current_path = path
                return self.current_obj.current_path + self.current_obj.create_encoding(), 3, 2

            elif child.name == name and child.type == '[FILE]':
                path = self.current_obj.current_path
                self.current_obj = child
                path += '/' + child.name
                self.current_obj.current_path = path
                return self.current_obj.current_path + ' ' + child.view_content(), 3, 2

        return '', 4, 4

    def save(self, name):
        name_content = name.split("\x00")
        if self.current_obj.type == "[FILE]":
            if name_content[0] == self.current_obj.name:
                self.current_obj.save_into_file(name_content[1])
                return '', 4, 2
            return '', 4, 4
        return '', 5, 4

    def new_file(self, name):
        if self.current_obj.type == "[DIRECTORY]":
            self.current_obj.add_child(File(name, self.current_obj, self.current_obj.level + 1))
            return '', 1, 2
        return '', 5, 4

    def new_directory(self, name):
        if self.current_obj.type == "[DIRECTORY]":
            self.current_obj.add_child(Directory(name, self.current_obj, self.current_obj.level + 1))
            return '', 1, 2
        return '', 5, 4

    def delete(self, name):
        for child in self.current_obj.children:
            if child.name == name:
                self.current_obj.children.remove(child)
                return '', 2, 2
        return '', 4, 4
