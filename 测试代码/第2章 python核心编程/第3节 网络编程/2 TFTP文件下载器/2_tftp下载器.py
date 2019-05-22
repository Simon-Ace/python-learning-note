from socket import *
import struct
import os


def main():
    file_name = input("please input file name: ")

    # 1 构建socket
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    # udp_socket.bind(("", 7777))

    # 2 发送请求
    request_file_code = struct.pack("!H%dsb5sb"%len(file_name), 1, bytes(file_name.encode('utf-8')), 0, b"octet", 0)  #octet: 8位为一组
    udp_socket.sendto(request_file_code, ("192.168.25.3", 69))

    err_trans = False   #标记是否错误传输
    block_num_done = 1

    with open(file_name, 'wb') as f:
        while True:
            # 3 接收数据
            recv_data, recv_ip = udp_socket.recvfrom(1024)
            op_code = struct.unpack("!H", recv_data[0:2])[0]    #取出操作码

            if op_code == 3:
                # 正常请求
                # 4 返回响应
                block_num_recv = struct.unpack("!H", recv_data[2:4])[0]
                respond_code = struct.pack("!HH", 4, block_num_recv)
                udp_socket.sendto(respond_code, recv_ip)

                if block_num_done == block_num_recv:
                    f.write(struct.unpack("!%ds"%len(recv_data[4:]), recv_data[4:])[0])
                    block_num_done = (block_num_done + 1) % 65536

                    if block_num_done % 1000 == 0:
                        print(block_num_done)

                if len(recv_data) < 516:
                    break
            elif op_code == 5:
                # 错误请求
                print("[err code: %s] %s" % (struct.unpack("!H", recv_data[2:4])[0],
                                             struct.unpack("!%ds" % (len(recv_data) - 6), recv_data[4:-2])[0].decode("utf-8")))
                err_trans = True
                break
            else:
                # 未知情况
                print("unknown error!")
                err_trans = True
                break

    if err_trans:
        print("error transmission")
        os.unlink(file_name)
    else:
        print("Transmission complete!")


if __name__ == '__main__':
    main()


# 写个循环重复接收
# 当recv_data数据长度小于516跳出循环
# 向文件中写入
# 若请求错误，则删除文件
# 错误重传的检查
# 大文件的块标号循环

# (ip.src==192.168.25.3 and ip.dst==192.168.25.4) or (ip.src==192.168.25.4 and ip.dst==192.168.25.3)