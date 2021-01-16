import socket
import threading
from CoAPMessage import CoAPMessage
import interface
from queue import Queue

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, root):
        threading.Thread.__init__(self)
        self.client_messageQ = Queue()
        self.csocket = clientsocket
        self.address = clientAddress
        self.root = root
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from: ", self.address)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        self.root.labelConnection.config(text=f"clientul {str(self.address)} s-a conectat")
        self.csocket.send(b"Welcome to the server!")
        while True:

            msg = self.csocket.recv(8092)
            if not msg: break
            print(msg)
            if CoAPMessage.from_bytes(msg).msg_type == 1:
                self.csocket.send(bytes(str(CoAPMessage("confirmation", 0, 2, CoAPMessage.from_bytes(msg).msg_code, 1)), "utf-8"))
            # print(CoAPMessage.from_bytes(msg).header_version)
            self.client_messageQ.put(CoAPMessage.from_bytes(msg).payload)
            print(CoAPMessage.from_bytes(msg))
            # self.client_messageQ.put(msg)
            # self.root.labelMesaj1.config(text=f"mesaj: " + self.client_messageQ.get())
            # self.root.labelMesaj2.config(text=f"mesaj: " + self.client_messageQ.get())
            while not self.client_messageQ.empty():
                print('new')
                self.root.labelMesaj[self.root.indexMesaj].config(text=f"mesaj: " + self.client_messageQ.get())
                self.root.indexMesaj = self.root.indexMesaj + 1
                print(self.client_messageQ)
        print ("Client at ", self.address, " disconnected...")

class Server():
    def __init__(self, root):
        self.coada_clienti = Queue()
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
            clientsock, clientAddress = s.accept()
            #if str(clientAddress) != str(self.coada_clienti.get()):
                #self.coada_clienti.put(clientAddress)
            newthread = ClientThread(clientAddress, clientsock, self.root)
            newthread.start()
            # now our endpoint knows about the OTHER endpoint.
            # clientsocket, address = s.accept()

            # daca este acelasi client care se conecteaza nu mai afisam
            '''if self.client_connection != address:
                # modifical labelConnection din interface sa afiseze adresa
                self.root.labelConnection.config(text=f"clientul {str(address)} s-a conectat")

            # daca clientul se conecteaza/deconecteaza nu se va mai afisa
            self.client_connection = str(address)

            # mesaj trimis la client
            clientsocket.send(b"Salut!")

            #primim mesajul intr un buffer de 8092
            while True:
                msg = clientsocket.recv(8092)
                print(str(msg))
                if not msg: break
                self.client_messageQ.put(CoAPMessage.from_bytes(msg).payload)
                print(CoAPMessage.from_bytes(msg).payload)
                #self.client_messageQ.put(msg)
                #self.root.labelMesaj1.config(text=f"mesaj: " + self.client_messageQ.get())
                #self.root.labelMesaj2.config(text=f"mesaj: " + self.client_messageQ.get())
                i = 0
                while not self.client_messageQ.empty():
                    print('new')
                    self.root.labelMesaj[i].config(text=f"mesaj: " + self.client_messageQ.get())
                    i = i + 1''

            ''d = {1:"hi", 2: "there"}
            msg = pickle.dumps(d)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
            print(msg)
            clientsocket.send(msg)''

    def getConnection(self, msg):
        self.display_connection_thread = threading.Thread(target=lambda: self.root.add_label(msg)).start()'''