import FileSys
import socket

class Server:
    def __init__(self):
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host,
        # and a well-known port
        serversocket.bind((socket.gethostname(), 1234))
        # become a server socket
        serversocket.listen(5)

        while True:
            # accept connections from outside
            (clientsocket, address) = serversocket.accept()
            # now do something with the clientsocket
            clientsocket.send(bytes("Hello but in coap protocol"))

            command = clientsocket.recv(16)
            clientsocket.close()


