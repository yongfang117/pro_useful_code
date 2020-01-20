#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import socket
import threading
import socketserver
import json


def make_request_message():
    # 消息体
    # 请求设备列表消息
    device_request_message = {
        "command": "device",
        "data": {}
    }
    # 设备启动请求消息
    device_start_request_message = {
        "command": "device_start",
        "data":
            {
                "device": "device_test"
            }
    }

    # 设备停止请求消息
    device_stop_request_message = {
        "command": "device_stop",
        "data":
            {
                "device": "device_test"
            }
    }
    # 模块启动请求消息
    mod_start_request_message = {
        "command": "mod_start",
        "data":
            {
                "device": "device_test",
                "mod": "mod_test"
            }
    }

    # 模块停止请求消息
    mod_stop_request_message = {
        "command": "mod_stop",
        "data":
            {
                "device": "device_test",
                "mod": "mod_test"
            }
    }
    num = int(input("请输入数字:"))
    if num == 1:
        request_message = device_request_message
    if num == 2:
        request_message = device_start_request_message
    if num == 3:
        request_message = device_stop_request_message
    if num == 4:
        request_message = mod_start_request_message
    if num == 5:
        request_message = mod_stop_request_message
    return request_message


# def client(ip, port, request_message):
def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        request_message = make_request_message()
        # 客户端发送请求消息
        request_msg = "{}\n".format(json.dumps(request_message))
        print("Send command: {}".format(request_msg))
        sock.sendall(request_msg.encode("utf-8"))

        # 客户端接收消息
        recv_data = sock.recv(1024)
        # print(recv_data)
        recv_content = recv_data.decode("utf-8")
        print("接收服务端的数据为:{}".format(recv_content))
        # import pdb;pdb.set_trace()
        msg = recv_content.split("\n")[0]
        # print(msg)
        payload = json.loads(msg)
        # print(payload)
    except Exception as e:
        print(e)

    finally:
        sock.close()


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 9000
    # HOST, PORT = "10.6.0.66", 9000
    # request_message = {
    #     #     "command": "device",
    #     #     "data": {}
    #     # }

    # client(HOST, PORT, request_message)
    client(HOST, PORT)
