#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import socket
import threading
import socketserver
import json, types, string
import os, time
# import config


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # 请求设备列表回复消息
        device_response_message = {"command": "device",
                                   "response": {
                                       "devices":
                                           [
                                               "device_test",
                                               "device_01",
                                               "device_02"
                                           ],
                                       "errors":
                                           [
                                               # {
                                               #     "device_name": "device_test",
                                               #     "errs":
                                               #         [
                                               #             {
                                               #                 "err_no": 0,
                                               #                 "err_info": "成功"
                                               #             }, {
                                               #             "err_no": 0,
                                               #             "err_info": "失败"
                                               #         }
                                               #         ]
                                               # },
                                               {
                                                   "device_name": "device_01",
                                                   "errs":
                                                       [
                                                           {
                                                               "err_no": 0,
                                                               "err_info": "成功"
                                                           }, {
                                                           "err_no": 1,
                                                           "err_info": "失败"
                                                       }
                                                       ]
                                               },
                                               {
                                                   "device_name": "device_02",
                                                   "errs":
                                                       [
                                                           {
                                                               "err_no": 3,
                                                               "err_info": "成功"
                                                           }, {
                                                           "err_no": 5,
                                                           "err_info": "失败"
                                                       }
                                                       ]
                                               }

                                           ]
                                   }
                                   }

        # 设备启动回复消息
        device_start_response_message = {
            "command": "device_start",
            "response": {
                "err_no": 5
            }
        }
        # 设备停止回复消息
        device_stop_response_message = {
            "command": "device_stop",
            "response": {
                "err_no": 0
            }
        }
        # 模块启动回复消息
        mod_start_response_message = {
            "command": "mod_start",
            "response": {
                "err_no": 3
            }
        }
        # 模块停止回复消息
        mod_stop_response_message = {
            "command": "mod_stop",
            "response": {
                "err_no": 0
            }
        }
        try:
            # 服务端接收消息
            recv_data = self.request.recv(1024)
            # print(recv_data)
            recv_content = recv_data.decode("gbk")
            print("接收客户端的消息为:{}".format(recv_content))
            msg = recv_content.split("\n")[0]
            # print(msg)
            payload = json.loads(msg)
            # print(payload)
            command = payload['command']
            if command == "device":
                response_message = device_response_message
            if command == "device_start":
                response_message = device_start_response_message
            # import pdb;pdb.set_trace()
            if command == "device_stop":
                response_message = device_stop_response_message
            if command == "mod_start":
                response_message = mod_start_response_message
            if command == "mod_stop":
                response_message = mod_stop_response_message

            # 服务端发送回复消息
            response_msg = "{}\n".format(json.dumps(response_message))
            print("Send: {}".format(response_msg))
            self.request.sendall(response_msg.encode("gbk"))
        except Exception as e:
            print(e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "", 9000

    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
