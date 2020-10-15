import pickle
import socket

import cv2

# Todo Compress video

try:
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 9000))
        s.send('Hello'.encode())

        data_str = b''
        while True:
            data = s.recv(512)
            if len(data) < 1:
                break
            data_str += data
        s.close()
        byte_data = pickle.loads(data_str)
        cv2.imshow("frame", byte_data)
        cv2.waitKey(1)

except KeyboardInterrupt as e:
    cv2.destroyAllWindows()
    s.close()

except:
    cv2.destroyAllWindows()
    s.close()
