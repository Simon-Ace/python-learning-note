"""
tcp简单服务器
"""
from socket import *

# SOCK_STREAM表示tcp通信
serverSocket = socket(AF_INET, SOCK_STREAM)

# 绑定端口
serverSocket.bind(("", 7788))

# 将主动套接字变为被动套接字
serverSocket.listen(5)

# 等待连接
clientSocket, clientInfo = serverSocket.accept()

# 等待收数据
recv_data = clientSocket.recv(1024)

print("%s: %s" % clientInfo, recv_data.decode("gb2312"))

serverSocket.close()
clientSocket.close()