from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(("192.168.25.3", 7788))

clientSocket.send(b'haha')
recv_data = clientSocket.recv(1024)
print(recv_data)

clientSocket.close()