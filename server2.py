from queue import Queue
import socket
import threading
from CoAPMessage import CoAPMessage, CoAP


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, message, root, UDPServerSocket):
        threading.Thread.__init__(self)
        self.UDPServerSocket = UDPServerSocket
        self.client_messageQ = Queue()
        self.message = message
        self.address = clientAddress
        self.root = root
        print("New message received from: ", clientAddress)

    def run(self):
        self.root.labelConnection.config(text=f"clientul {str(self.address)} a trimis un mesaj")
        while True:
            if CoAPMessage.from_bytes(self.message).msg_type == CoAP.TYPE_CONF:
                coap_message = CoAPMessage.from_bytes(self.message)
                coap_message.payload = 'd/mnt/\x00fBD Proiect\x00fRC\x00dporn\x00dsecrets\x00'
                55 01 00 02 00 00 00 7c b3 ff b'\x05asda'
                coap_message.msg_type = CoAP.TYPE_ACK
                coap_message.msg_class = CoAP.CLASS_SUCCESS
                coap_message.msg_code = 1

                bytes_to_send = CoAP.wrap(coap_message)
                self.UDPServerSocket.sendto(bytes_to_send, self.address)

            self.client_messageQ.put(CoAPMessage.from_bytes(self.message).payload)
            while not self.client_messageQ.empty():
                self.root.labelMesaj[self.root.indexMesaj].config(text=f"mesaj: " + self.client_messageQ.get())
                self.root.indexMesaj = self.root.indexMesaj + 1
                print(self.client_messageQ)


class Server():
    def __init__(self, root):
        self.localIP = "127.0.0.1"
        self.localPort = 5000
        self.coada_clienti = Queue()
        self.is_running = False
        self.root = root
        self.buffersize = 4096
        self.client_connection = ""
        self.client_messageQ = Queue()
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.UDPServerSocket.bind((self.localIP, self.localPort))

    def run(self):
        self.is_running = True

        while self.is_running:
            message, clientAddress = self.UDPServerSocket.recvfrom(self.buffersize)
            newthread = ClientThread(clientAddress, message, self.root, self.UDPServerSocket)
            newthread.start()
