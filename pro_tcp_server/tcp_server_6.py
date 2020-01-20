#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import socket
import threading
import socketserver
import json, types, string
import os, time


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        jdata = json.loads(data.decode('utf-8'))
        print("Receive data from '%r'" % (data))
        print("Receive jdata from '%r'" % (jdata))
        rec_request = jdata[0]['command']
        cur_thread = threading.current_thread()
        response = [{
            "command": "device",
            "response": {
                "devices": [
                    "device_test",
                    "device_01",
                    "device_02"
                ],
                "errors": [{
                    "device_name": "device_test",
                    "errs": [{
                        "err_no": 0,
                        "err_info": "成功"
                    }
                        # {
                        # "err_no":1,
                        # "err_info":"失败"
                        # }
                    ]
                }
                ]
            }
        }
        ]

        jresp = json.dumps(response)
        self.request.sendall(jresp.encode('utf-8'))
        # rec_cmd = "proccess "+rec_src+" -o "+rec_dst
        # print ("CMD '%r'" % (rec_cmd))
        # os.system(rec_cmd)


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
