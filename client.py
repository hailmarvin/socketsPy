import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

# Maintain Connection
while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(8)
        if new_msg:
            print("new msg len:", msg[:HEADERSIZE])
            msg_len = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full msg len: {msg_len}")    
        full_msg += msg.decode("utf-8")
        print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msg_len:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ""