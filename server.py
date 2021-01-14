import socket
from CoAPMessage import CoAPMessage
import interface
from queue import Queue


class Server():
    def __init__(self, root):
        self.is_running = False
        self.root = root
        self.client_connection = ""
        self.client_messageQ = Queue()

    def run(self):
        self.is_running = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1234))
        s.listen(5)

        while self.is_running:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = s.accept()

            # daca este acelasi client care se conecteaza nu mai afisam
            if self.client_connection != address:
                # modifical labelConnection din interface sa afiseze adresa
                self.root.labelConnection.config(text=f"clientul {str(address)} s-a conectat")

            # daca clientul se conecteaza/deconecteaza nu se va mai afisa
            self.client_connection = str(address)

            # mesaj trimis la client
            clientsocket.send(b"Salut!")

            #primim mesajul intr un buffer de 4096
            msg = clientsocket.recv(4096)
            if not msg: break
            self.client_messageQ.put(CoAPMessage.from_bytes(msg).payload)

            self.root.labelMesaj.config(text=f"mesaj: " + self.client_messageQ.get())

            '''d = {1:"hi", 2: "there"}
            msg = pickle.dumps(d)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
            print(msg)
            clientsocket.send(msg)'''

    '''def getConnection(self, msg):
        self.display_connection_thread = threading.Thread(target=lambda: self.root.add_label(msg)).start()'''
