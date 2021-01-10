import socket

# AF_INET == ipv4 (family/domain)
# SOCK_STREAM == tcp (type)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#setting up localhost
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Hello there!!!","utf-8"))
    clientsocket.close()