import socket
import time

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

    msg = "Welcome to the server!!!"
    msg = f"{len(msg):<{HEADERSIZE}}"+msg
    clientsocket.send(bytes(msg,"utf-8"))

    while True:
        time.sleep(3)
        msg = f"The time is {time.time()}"
        msg = f"{len(msg):<{HEADERSIZE}}"+msg

        print(msg)

        clientsocket.send(bytes(msg,"utf-8"))