import json
import socket

from Chat import Chat

DATABASE_NAME = 'database.sqlite'
HOST = 'localhost'
PORT = 9000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    while True:
        (clientSocket, address) = server_socket.accept()
        data_str = clientSocket.recv(5000).decode()
        js = json.loads(data_str)
        user_name = js['username']
        password = js['password']

        chat = Chat(DATABASE_NAME)
        data_to_send = {}
        if not chat.verify(user_name, password):
            data_to_send['status'] = False
            clientSocket.send(json.dumps(data_to_send).encode())
            clientSocket.close()
            continue

        data_to_send['status'] = True  # TODO some awesome verification, AES keys?
        messages = chat.read_msg(2)
        messages.reverse()
        data_to_send['chats'] = messages
        clientSocket.send(json.dumps(data_to_send).encode())
        clientSocket.close()


except KeyboardInterrupt:
    server_socket.close()

except Exception as e:
    print(e)
    server_socket.close()
