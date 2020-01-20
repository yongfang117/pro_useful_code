# -*- coding: utf-8 -*-
"""
时间: 2019/12/26 20:31

作者: lixianchun@cyai.com

更改记录:

重要说明:
"""

import json
import socket


if __name__ == '__main__':
    # tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # spurt code
    # tcp_client_socket.connect(("127.0.0.1", 5000))
    # send_data = "DD:1\r\n".encode("utf-8")
    # send_data = "DS:1\r\n".encode("utf-8")
    # send_data = "RD:2019,sn1,,sn3\r\n".encode("utf-8")
    # send_data = "RD:2019,sn1,sn2,sn3\r\n".encode("utf-8")
    # send_data = "RD:2020,sn1,sn2,sn3\r\n".encode("utf-8")
    # send_data = "RD:2020,sn1,sn2,sn3\r\n".encode("utf-8")
    # send_data = "OP:1,13\r\n".encode("utf-8")

    # # cut feet
    # tcp_client_socket.connect(("127.0.0.1", 5001))
    # send_data = "DS:1\r\n".encode("utf-8")
    # send_data = "RD:2019,1,2,1\r\n".encode("utf-8")

    # aoi
    # tcp_client_socket.connect(("127.0.0.1", 5002))
    # send_data = "DS:1\r\n".encode("utf-8")
    # pos1 = json.dumps({"result": "NG", "N01": 1, "N02": 2, "N03": 1, "N04": 1, "N05": 1, "N06": 1, "N07": 1, "N08": 2, "N09": 1, })
    # pos2 = json.dumps({})
    # pos3 = json.dumps({"result": "OK", "N01": 2, "N02": 2, "N03": 2, "N04": 2, "N05": 2, "N06": 2, "N07": 2, "N08": 2, "N09": 2, })
    # send_data = f'RD:2019,[{pos1},{pos2},{pos3}]\r\n'.encode("utf-8")

    # clamp
    # tcp_client_socket.connect(("127.0.0.1", 5003))
    # send_data = "DS:1\r\n".encode("utf-8")
    # send_data = "RD:2019,1,2,1\r\n".encode("utf-8")

    # fct
    # tcp_client_socket.connect(("127.0.0.1", 5004))
    # send_data = "DS:1\r\n".encode("utf-8")
    # send_data = "RT:2019\r\n".encode("utf-8")

    # fct1
    # tcp_client_socket.connect(("127.0.0.1", 5006))
    res1 = json.dumps({"sn": "sn1",
                       "result": "PASS",
                       "detail": {
                           "VSP-GND不良(KΩ)": 171.8,
                           "VCC-GND不良(KΩ)": 32.52,
                           "VM-GND不良(KΩ)": 8.82,
                           "VCC不良()": 14.99,
                           "VCC不良()": 6.97,
                           "VCC不良(V)": 0.1,
                           "VM不良(V)": 309.54,
                           "VSP不良()": 15,
                           "VSP不良()": 9.97,
                           "VSP不良(V)": 3,
                           "实际转速不良(RPM)": 392.328,
                           "旋转方向不良(°)": -89,
                           "FG频率不良(Hz)": 78.65,
                           "FG占空比不良(%)": 53.23,
                           "FG高电平不良(V)": 14.55,
                           "FG低电平不良(V)": -0.12,
                           "VM-CURR(A)": 0.07,
                           "VCC-CURR()": 0.02,
                           "VCC-CURR()": 0.099,
                           "VCC-CURR(A)": 0,
                           "VCC-GND停电电阻不良(KΩ)": 133.929
                       }}, ensure_ascii=False)
    res2 = json.dumps({}, ensure_ascii=False)
    res3 = json.dumps({"sn": "sn3",
                       "result": "FAIL",
                       "detail": {
                           "VSP-GND不良(KΩ)": 164.6,
                           "VCC-GND不良(KΩ)": 1051.7
                       }}, ensure_ascii=False)
    # send_data = f'RD:{res1}\r\n'.encode("utf-8")

    # fct2
    # tcp_client_socket.connect(("127.0.0.1", 5007))
    # send_data = f'RD:{res2}\r\n'.encode("utf-8")

    # fct3
    # tcp_client_socket.connect(("127.0.0.1", 5008))
    # send_data = f'RD:{res3}\r\n'.encode("utf-8")

    # 0ffline
    # tcp_client_socket.connect(("127.0.0.1", 5005))
    # send_data = "DS:1\r\n".encode("utf-8")
    # send_data = "RD:2019,1,2,1\r\n".encode("utf-8")
    # send_data = "OP:1,13\r\n".encode("utf-8")

    # tcp_client_socket.send(send_data)
    # recv_data = tcp_client_socket.recv(1024)
    # print(recv_data)
    # recv_content = recv_data.decode("utf-8")
    # print("接收服务端的数据为:", recv_content)
    # # 关闭套接字
    # tcp_client_socket.close()
    import time

    tcp_client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # fct
    tcp_client_socket1.connect(("127.0.0.1", 5000))
    send_data = "DS:1\r\n".encode("utf-8")
    tcp_client_socket1.send(send_data)
    while True:
        time.sleep(2)
        recv_data1 = tcp_client_socket1.recv(1024)

        if "DS" in recv_data1.decode("utf-8"):
            print("DS response: ", recv_data1)
        if len(recv_data1) == 0:
            continue
        if "CF" in recv_data1.decode("utf-8"):
            print("CF request: ", recv_data1)
            send_data1 = "CF:1\r\n".encode("utf-8")
            print("CF response: ", send_data1)
            tcp_client_socket1.send(send_data1)

    tcp_client_socket1.close()
