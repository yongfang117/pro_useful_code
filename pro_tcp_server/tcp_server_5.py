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
        # rec_src = jdata[0]['src']
        # rec_dst = jdata[0]['dst']
        rec_request = jdata[0]['request']

        cur_thread = threading.current_thread()
        # response = [{'thread':cur_thread.name,'src':rec_src,'dst':rec_dst}]
        response = [{
            "robot_name": "ur5",
            "position": {
                "x": 10,
                "y": 10,
                "z": 10,
                "a": 10,
                "b": 10,
                "c": 10
            },
            "joint_states": {
                "j1": 10,
                "j2": 10,
                "j3": 10,
                "j4": 10,
                "j5": 10,
                "j6": 10
            },
            "robot_status": 1,
            "io": {
                "io1": 1,
                "io2": 0,
                "io3": 1,
                "io4": 0,
                "io5": 1,
                "io6": 0,
                "io7": 1,
                "io8": 0
            }
        }]

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
