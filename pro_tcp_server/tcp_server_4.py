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
        jdata = json.loads(data)
        print("Receive data from '%r'" % (data))
        print("Receive jdata from '%r'" % (jdata))

        rec_src = jdata[0]['src']
        rec_dst = jdata[0]['dst']
        cur_thread = threading.current_thread()

        response = [{'thread': cur_thread.name, 'src': rec_src, 'dst': rec_dst}]
        jresp = json.dumps(response)
        self.request.sendall(jresp)
        rec_cmd = "proccess " + rec_src + " -o " + rec_dst
        print("CMD '%r'" % (rec_cmd))
        os.system(rec_cmd)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "", 9000

    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
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
