import socket

# AF_NET == ipv4 (family/domain)
# SOCK_STREAM == tcp (type)
s = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
#setting up localhost
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")