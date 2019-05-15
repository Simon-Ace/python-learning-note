from threading import Thread
from socket import *


def send_msg(ip_port):
    while 1:
        msg = input(">> send message: ")
        udp_socket.sendto(msg.encode("utf-8"), ip_port)

def recv_msg():
    while 1:
        recv_data = udp_socket.recvfrom(1024)
        print("\r<< receive message [%s]: %s" % (recv_data[1], recv_data[0].decode("utf-8")))
        #print函数会先将数据读入一个缓冲区，直到遇到\n或者数据达到缓冲区大小(这里是8KB)，才将数据写入sys.stdout
        print(">> send message: ", end='', flush=True)

udp_socket = socket(AF_INET, SOCK_DGRAM)

def main():
    global udp_socket

    udp_socket.bind(("", 7777))

    ip = input(">> please input target ip: ")
    if not ip:
        ip = "192.168.25.3"
    port = input(">> please input target port: ")
    ip_port = (ip, int(port))

    t_send = Thread(target=send_msg, args=(ip_port,))
    t_recv = Thread(target=recv_msg)

    t_send.start()
    t_recv.start()

    t_send.join()
    t_recv.join()

if __name__ == '__main__':
    main()


# 参数提示 ctrl+p