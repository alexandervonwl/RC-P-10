import socket
import time
from CoAPMessage import *
import time

HEADERSIZE = 10
localIP = "127.0.0.1"
localPort = 4999
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((localIP, localPort))

s.sendto(CoAP.wrap(CoAPMessage('\x05abc', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 3)), (localIP, 5000))
time.sleep(2)
s.sendto(CoAP.wrap(CoAPMessage('\x02abc', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 4)), (localIP, 5000))
time.sleep(2)
s.sendto(CoAP.wrap(CoAPMessage('\x04file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 5)), (localIP, 5000))
time.sleep(2)
s.sendto(CoAP.wrap(CoAPMessage('\x02file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 6)), (localIP, 5000))
message, clientAddress = s.recvfrom(4096)

print(CoAPMessage.from_bytes(message))

'''while True:
    msg = s.recv(16)
    print(msg)
    if new_msg:
        print("new msg len:",msg[:HEADERSIZE])
        msglen = int(msg[:HEADERSIZE])
        new_msg = False

    print(f"full message length: {msglen}")

    full_msg += msg.decode("utf-8")

    print(len(full_msg))


    if len(full_msg)-HEADERSIZE == msglen:
        print("full msg recvd")
        print(full_msg[HEADERSIZE:])
        new_msg = True
        full_msg = "" '''