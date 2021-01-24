import socket
import time
from cv2 import cv2
import numpy as np
 
def ReceiveVideo():
    address = ('127.0.0.1', 1234)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(1)
 
    def recvall(sock, count):
        data = b''
        while count:
            newdata = sock.recv(count)

            if not newdata:
                return None

            data += newdata
            count -= len(newdata)
        return data

    conn, addr = s.accept()
    print('connect from:'+str(addr))
    while 1:
        start = time.time()
        length = recvall(conn,16)

        stringData = recvall(conn, int(length))
        data = np.frombuffer(stringData, np.uint8)
        frame = cv2.imdecode(data,cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (640, 480))
        cv2.imshow('LiveView', frame)

        end = time.time()
        seconds = end - start
        fps  = 1/seconds
        conn.send(bytes(str(int(fps)),encoding='utf-8'))
        k = cv2.waitKey(10)&0xff
        if k == 27:
            break

    s.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ReceiveVideo()


# data = b''
# payload_size = struct.calcsize("L") 
# conn,addr=s.accept()
# while True:
    # while len(data) < payload_size:
    #     data += conn.recv(4096)

    # packed_msg_size = data[:payload_size]
    # data = data[payload_size:]
    # msg_size = struct.unpack("L", packed_msg_size)[0]

    # while len(data) < msg_size:
    #     data += conn.recv(4096)

    # frame_data = data[:msg_size]
    # data = data[msg_size:]

    # frame=pickle.loads(frame_data)
    # frame = cv2.resize(frame, (640, 480)) 
    # cv2.imshow('frame',frame)
    # cv2.waitKey(0)

# cv2.destroyAllWindows()