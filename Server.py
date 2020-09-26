import json
import socket

from Chat import Chat

chat = Chat('database.sqlite')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind(('localhost', 9000))
    server_socket.listen(5)
    while True:
        (clientSocket, address) = server_socket.accept()
        rd = clientSocket.recv(5000).decode()
        js = json.loads(rd)
        user_name = js['username']
        password = js['password']
        chat.verify(user_name, password)


except KeyboardInterrupt:
    server_socket.close()
