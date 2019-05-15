"""
对端口进行绑定

使收发只通过指定的端口进行，不使用系统随机分配的端口
一般只对接收方的端口进行绑定
"""

from socket import *

udpsocket = socket(AF_INET, SOCK_DGRAM)
udpsocket.bind(("", 7777)) #第一个是ip地址，空表示本机ip

# 发送
# udpsocket.sendto(b"constant port data", ('192.168.25.3', 8080))

# 接收
while 1:
    recv_data = udpsocket.recvfrom(1024)
    print(recv_data[0], '-----', recv_data[1])

