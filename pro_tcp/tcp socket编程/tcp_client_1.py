import socket

"""
TCP 通信步骤:
        创建连接
        传输数据
        关闭连接
"""

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## 1. AF_INET：表示ipv4  # 2. SOCK_STREAM: tcp传输协议
    sock.connect(("127.0.0.1", 5000))

    send_data = "你好服务端，我是客户端!".encode("utf-8")
    sock.send(send_data)

    recv_data = sock.recv(1024)
    print(recv_data)
    recv_content = recv_data.decode("utf-8")
    print("接收服务端的数据为:", recv_content)

    sock.close()  # 关闭套接字
