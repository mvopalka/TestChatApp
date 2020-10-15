import pickle
import socket

import cv2

# Todo Compress video

DATABASE_NAME = 'database.sqlite'
HOST = 'localhost'
PORT = 9000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    while True:
        (clientSocket, address) = server_socket.accept()
        cap = cv2.VideoCapture(0)
        data_str = clientSocket.recv(5000).decode()
        ret, frame = cap.read()
        data = pickle.dumps(frame)
        print("Data len:", len(data))
        cap.release()
        clientSocket.send(data)
        clientSocket.close()


except KeyboardInterrupt:
    server_socket.close()

except Exception as e:
    print(e)
    server_socket.close()
