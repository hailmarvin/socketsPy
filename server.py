import socket
import time
import pickle

HEADERSIZE = 10

# AF_INET == ipv4 (family/domain)
# SOCK_STREAM == tcp (type)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#setting up localhost
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    d = {1: "Hello", 2: "There"}
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8")+msg
    print(msg)
    clientsocket.send(msg)