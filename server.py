import socket
from CoAPMessage import CoAPMessage
import interface


class Server():
    def __init__(self, root):
        self.is_running = False
        self.label = "abcd"
        self.root = root
        # self.root = root

    def run(self):
        self.is_running = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1234))
        s.listen(5)

        while self.is_running:
            # now our endpoint knows about the OTHER endpoint.

            clientsocket, address = s.accept()
            self.root.labelConnection.config(text=f"clientul {str(address)} s-a conectat")
            # print(self.label)
            # print(f"Connection from {address} has been established.")
            clientsocket.send(b"Salut!")
            msg = clientsocket.recv(4096)
            if not msg: break
            print(CoAPMessage.from_bytes(msg))
            interface.interface.msg = msg
            # self.getConnection(msg)

            '''d = {1:"hi", 2: "there"}
            msg = pickle.dumps(d)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
            print(msg)
            clientsocket.send(msg)'''

    '''def getConnection(self, msg):
        self.display_connection_thread = threading.Thread(target=lambda: self.root.add_label(msg)).start()'''
