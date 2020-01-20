#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import socket
import threading
import socketserver
import json


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    try:
        print("Send: {}".format(message))
        sock.sendall(message.encode("utf-8"))

        response = sock.recv(1024)
        jresp = json.loads(response.decode('utf-8'))
        print("Recv: ", jresp)

    finally:
        sock.close()


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 9000
    msg = [{"request": 1}]
    jmsg = json.dumps(msg)
    client(HOST, PORT, jmsg)
