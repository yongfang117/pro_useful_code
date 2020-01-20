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
        print("Receive jdata from '%r'" % (jdata))

        response = [{"robot_name": "ur5"}]
        jresp = json.dumps(response)
        self.request.sendall(jresp.encode('utf-8'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "", 9000

    socketserver.TCPServer.allow_reuse_address = True #设置地址复用
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)  #?
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")

    # Activate the server; this will keep running until you interrupt the program with Ctrl-C
    server.serve_forever()
