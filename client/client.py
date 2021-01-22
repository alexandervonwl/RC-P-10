import socket
import time
from CoAPMessage import *
import time

HEADERSIZE = 10
localIP = "127.0.0.1"
localPort = 4999
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((localIP, localPort))

# cream director dir1
s.sendto(CoAP.wrap(CoAPMessage('\x05dir1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 3, 0x1, 0x2, 0x3)), (localIP, 5000))
message1, clientAddress0 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)


# deschidem directorul dir1
s.sendto(CoAP.wrap(CoAPMessage('\x02dir1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 4)), (localIP, 5000))
message1, clientAddress1 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# cream in dir1 fisierul d1file1
s.sendto(CoAP.wrap(CoAPMessage('\x04d1file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 5)), (localIP, 5000))
message1, clientAddress2 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# deschidem fisierul d1file1
s.sendto(CoAP.wrap(CoAPMessage('\x02d1file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 6)), (localIP, 5000))
message1, clientAddress3 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# salvam abcdefgh in d1file1
s.sendto(CoAP.wrap(CoAPMessage('\x03d1file1\x00abcdefghhb', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 7)), (localIP, 5000))
message1, clientAddress4 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# dam back, deci deschidem dir1
s.sendto(CoAP.wrap(CoAPMessage('\x01', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 8)), (localIP, 5000))
message1, clientAddress5 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# deschidem d1file 1 si ne afiseaza si continutul
s.sendto(CoAP.wrap(CoAPMessage('\x02d1file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 9)), (localIP, 5000))
message1, clientAddress6 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# dam iar back, ajungem in dir1
s.sendto(CoAP.wrap(CoAPMessage('\x01', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 10)), (localIP, 5000))
message1, clientAddress7 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# cream in dir1 fisierul d1file2
s.sendto(CoAP.wrap(CoAPMessage('\x04d1file2', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 11)), (localIP, 5000))
message1, clientAddress8 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# cream in dir1 directorul d1dir1
s.sendto(CoAP.wrap(CoAPMessage('\x05d1dir1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 12)), (localIP, 5000))
message1, clientAddress9 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# dam iar back, ajungem in root
s.sendto(CoAP.wrap(CoAPMessage('\x01', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 13)), (localIP, 5000))
message1, clientAddress10 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# cream director dir2
s.sendto(CoAP.wrap(CoAPMessage('\x05dir2', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 14)), (localIP, 5000))
message1, clientAddress11 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# deschidem directorul dir1
s.sendto(CoAP.wrap(CoAPMessage('\x02dir1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 15)), (localIP, 5000))
message1, clientAddress12 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# dau back, ajungem in root
s.sendto(CoAP.wrap(CoAPMessage('\x01', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 16)), (localIP, 5000))
message1, clientAddress13 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# deschidem directorul dir2
s.sendto(CoAP.wrap(CoAPMessage('\x02dir2', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 17)), (localIP, 5000))
message1, clientAddress14 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# cream in dir2 fisierul d2file1
s.sendto(CoAP.wrap(CoAPMessage('\x04d2file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 18)), (localIP, 5000))
message1, clientAddress15 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# cream in dir2 fisierul d2dir1
s.sendto(CoAP.wrap(CoAPMessage('\x05d2dir1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_POST, 19)), (localIP, 5000))
message1, clientAddress16 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# stergem din dir2 fisierul d2file1
s.sendto(CoAP.wrap(CoAPMessage('\x06d2file1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_DELETE, 20)), (localIP, 5000))
message1, clientAddress17 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# dau back, ajungem in root
s.sendto(CoAP.wrap(CoAPMessage('\x01', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_GET, 21)), (localIP, 5000))
message1, clientAddress18 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

# stergem din root dir1
s.sendto(CoAP.wrap(CoAPMessage('\x06dir1', CoAP.TYPE_CONF, CoAP.CLASS_METHOD, CoAP.CODE_DELETE, 22)), (localIP, 5000))
message1, clientAddress19 = s.recvfrom(4096)
print(CoAPMessage.from_bytes(message1))
time.sleep(1)

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