# -*- coding: utf-8 -*-
"""
时间: 2019/11/24 17:52
 
作者: lyf

更改记录:   

重要说明: 
"""
import paho.mqtt.client as mqtt

HOST = "10.6.3.29"
# HOST = "192.168.211.128"
PORT = 1883

def test():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    client.publish("chat","hello chenfulin",2)
    client.publish("chat", "你好", 2)
    client.publish("manager/uplink/response", "nihao", 2)
    client.publish("manager/uplink/response/r", "nihao_r")
    client.loop_forever()

if __name__ == '__main__':
    test()