import json
import socket

data = {}
data['username'] = 'admin'  # input("Enter username ")
data['password'] = 'password'  # input("Password")    # debug
# data['password'] = getpass()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9000))
s.send(json.dumps(data).encode())

data_str = ''
while True:
    data = s.recv(512)
    if len(data) < 1:
        break
    data_str += data.decode()

chat = json.loads(data_str)['chats']
for message in chat:
    if message[0]:
        print(message[1])
    else:
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", message[1])
print()
s.close()
