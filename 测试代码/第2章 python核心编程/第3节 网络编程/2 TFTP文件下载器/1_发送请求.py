from socket import *
import struct

udp_socket = socket(AF_INET, SOCK_DGRAM)

send_data = struct.pack("!H8sb5sb",1,b"test.jpg",0,b"octet",0)

udp_socket.sendto(send_data, ("192.168.25.3", 69))

udp_socket.close()