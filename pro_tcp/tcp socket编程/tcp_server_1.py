import socket

"""
基础 单任务
步骤说明:

    1. 创建服务端端套接字对象  socket()
    2.绑定端口号 bind()
    3.设置监听   listen()
    4.等待接受客户端的连接请求 accept()   service_client_socket, ip_port= 
    5.接收数据  recv()
    6.发送数据  send()
    7.关闭套接字 close()
"""

if __name__ == '__main__':
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  #设置端口号复用
    tcp_server_socket.bind(("", 5000))
    tcp_server_socket.listen(128)
    # 等待客户端建立连接的请求, 只有客户端和服务端建立连接成功代码才会解阻塞，代码才能继续往下执行
    # 1. 专门和客户端通信的套接字： service_client_socket
    # 2. 客户端的ip地址和端口号： ip_port
    service_client_socket, ip_port = tcp_server_socket.accept()  # 代码执行到此说明连接建立成功
    print("客户端的ip地址和端口号:", ip_port)

    recv_data = service_client_socket.recv(1024)  # 接收客户端发送的数据, 这次接收数据的最大字节数是1024
    recv_content = recv_data.decode("utf-8")
    print("接收客户端的数据为:", recv_content)

    send_data = "ok, 问题正在处理中...".encode("utf-8")
    service_client_socket.send(send_data)

    service_client_socket.close()  # 关闭服务与客户端的套接字， 终止和客户端通信的服务

    tcp_server_socket.close()  # 关闭服务端的套接字, 终止和客户端提供建立连接请求的服务
