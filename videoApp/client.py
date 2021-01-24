from cv2 import cv2
import numpy as np
import pickle
import socket
import sys
import struct
import time
from halo import Halo

def SendVideo():
    address = ('127.0.0.1', 1234)
    try:
        clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientsocket.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
 
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]

    while ret:
        time.sleep(0.01)
        _, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(imgencode)
        stringData = data.tobytes()

        clientsocket.send(str.encode(str(len(stringData)).ljust(16)))
        clientsocket.send(stringData)
        receive = clientsocket.recv(1024)
        ret, frame = capture.read()
        spinner = Halo(text='Streaming', spinner='bouncingBar', color='green', interval= 1)

        if receive:
            spinner.start()
        else:
            spinner.stop()
        if cv2.waitKey(10) == 27:
            break
    clientsocket.close()

if __name__ == '__main__':
    SendVideo()

# IP='127.0.0.1'
# PORT=1234

# cap = cv2.VideoCapture(0)
# clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# clientsocket.connect((IP, PORT))

# ret,frame=cap.read()
# while ret:
#     data = pickle.dumps(frame)
#     message_size = struct.pack("L", len(data))

#     print(frame)
#     clientsocket.send(message_size + data)

# cap.release()