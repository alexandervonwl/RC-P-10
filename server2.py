from queue import Queue
import socket
import threading
from CoAPMessage import CoAPMessage, CoAP
from FileSys import *


'''class ClientThread(threading.Thread):
    def __init__(self, clientAddress, message, root, UDPServerSocket):
        threading.Thread.__init__(self)
        self.UDPServerSocket = UDPServerSocket
        self.client_messageQ = Queue()
        self.message = message
        self.address = clientAddress
        self.root = root
        self.message_number = 0
        print("New message received from: ", clientAddress)

    def run(self):
        self.root.labelConnection.config(text=f"clientul {str(self.address)} a trimis un mesaj")
        while True:
            if CoAPMessage.from_bytes(self.message).msg_type == CoAP.TYPE_CONF:
                coap_message = CoAPMessage.from_bytes(self.message)
                coap_message.payload = 'd/mnt/\x00fBD Proiect\x00fRC\x00dporn\x00dsecrets\x00'
                55 01 00 02 00 00 00 7c b3 ff b'\x05asda'
                DecodePayload(FSComponent('root', None),coap_message.payload)
                coap_message.msg_type = CoAP.TYPE_ACK
                coap_message.msg_class = CoAP.CLASS_SUCCESS
                coap_message.msg_code = 1

                bytes_to_send = CoAP.wrap(coap_message)
                self.UDPServerSocket.sendto(bytes_to_send, self.address)

            self.client_messageQ.put(CoAPMessage.from_bytes(self.message).payload)
            while not self.client_messageQ.empty():
                self.root.labelMesaj[self.root.indexMesaj].config(text=f"mesaj: " + self.client_messageQ.get())
                self.root.indexMesaj = self.root.indexMesaj + 1
                print(self.client_messageQ)'''


class Server:
    def __init__(self, root):
        self.localIP = "127.0.0.1"
        self.localPort = 5000
        # self.coada_clienti = Queue()
        self.is_running = False
        self.root = root
        self.buffer_size = 4096
        self.client_connection = ""
        self.message_number = 0
        self.client_messageQ = Queue()
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.UDPServerSocket.bind((self.localIP, self.localPort))

    def run(self):
        self.is_running = True
        dp = DecodePayload(FSComponent('root', None), '')
        while self.is_running:
            message_rcv, client_address = self.UDPServerSocket.recvfrom(self.buffer_size)
            print(message_rcv)
            # newthread = ClientThread(clientAddress, message, self.root, self.UDPServerSocket)
            # newthread.start()
            self.root.label_connection.config(text=f"clientul {str(client_address)} a trimis un mesaj")
            coap_message_rcv = CoAPMessage.from_bytes(message_rcv)
            dp.payload = coap_message_rcv.payload
            message_send_payload, message_send_response_code, message_send_class = dp.parsePayload()
            message_send_class = CoAP.CLASS_SUCCESS
            message_send_code = 1
            message_send_token = coap_message_rcv.token
            if coap_message_rcv.msg_type == CoAP.TYPE_CONF:
                # coap_message_rcv.payload = 'd/mnt/\x00fBD Proiect\x00fRC\x00dporn\x00dsecrets\x00'
                message_send_type = CoAP.TYPE_ACK
                message_send_id = coap_message_rcv.msg_id
            else:
                message_send_type = CoAP.TYPE_NON_CONF
                message_send_id = self.message_number

            self.message_number += 1
            coap_message_send = CoAPMessage(message_send_payload, message_send_type, message_send_class,
                                            message_send_response_code, message_send_id, message_send_token)
            bytes_to_send = CoAP.wrap(coap_message_send)
            print(coap_message_send)
            self.UDPServerSocket.sendto(bytes_to_send, client_address)
            self.client_messageQ.put(coap_message_rcv.payload)
            while not self.client_messageQ.empty():
                self.root.label_message[self.root.index_message].config(text=f"mesaj: " + self.client_messageQ.get())
                self.root.index_message = self.root.index_message + 1
                print(self.client_messageQ)