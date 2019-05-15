"""
使用socket发送数据

在另一台Ubuntu电脑进行监听
sudo tcpdump udp port 8080 -A
"""

from socket import *

# AF_INET:用于 Internet 进程间通信; SOCK_STREAM（流式套接字，主要⽤于TCP协议）,SOCK_DGRAM（数据报套接字，主要用于 UDP 协议）

udpsocket = socket(AF_INET, SOCK_DGRAM)

# 使用UDP发送数据，每一次都要写上接收方的ip和port
udpsocket.sendto(b"what's that", ('192.168.25.3', 8080))
udpsocket.sendto(b"hello", ('192.168.25.3', 8080))

