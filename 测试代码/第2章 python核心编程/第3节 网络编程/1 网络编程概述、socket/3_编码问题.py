"""
编码问题

前面发送的时候，字符串前面都要加个b
这回是改成指定的编码方案，要注意的是，编解码的方式要相同
"""

from socket import *

udpsocket = socket(AF_INET, SOCK_DGRAM)

# udpsocket.sendto("厉害了".encode("utf-8"), ("192.168.25.3", 8080))

udpsocket.bind(("", 7777))

while 1:
    recv_data = udpsocket.recvfrom(1024)
    content, destInfo = recv_data
    print(content) #不解码的话，非一般asc字符会变成十六进制形式
    print(content.decode("gb2312")) #or "utf-8"