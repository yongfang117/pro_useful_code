# -*- coding: utf-8 -*-
"""
时间: 2019/11/24 17:53
 
作者: lyf

更改记录:   

重要说明: 
"""
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("chat")
    client.subscribe("manager/uplink/response/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload.decode("utf-8")))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.connect("127.0.0.1", 1883, 60)
# client.connect("192.168.211.128", 1883, 60)
client.connect("10.6.3.29", 1883, 60)
client.loop_forever()
