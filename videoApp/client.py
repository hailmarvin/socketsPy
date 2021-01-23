from cv2 import cv2
import numpy as np
import pickle
import socket
import sys
import struct

cap = cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))

while True:
    ret,frame=cap.read()

    data = pickle.dumps(frame)
    print(data)
    message_size = struct.pack("L", len(data))
    clientsocket.sendall(message_size + data)

    cv2.waitKey(0)

cap.release()