# -*- coding: utf-8 -*-
"""
时间: 2019/11/24 21:38
 
作者: lyf

更改记录:   

重要说明: 
"""
import datetime
import json
import logging
import os
import socket
import threading
import time

from paho.mqtt import client as mqtt_client


# logger = logging.getLogger('trk-proxy')
# logger.setLevel(logging.INFO)
#
# fmt = '%(asctime)s %(levelname)s %(filename)s %(lineno)s %(funcName)s %(message)s'
# ch = logging.StreamHandler()
# ch.setFormatter(logging.Formatter(fmt))
# fh = logging.FileHandler('log/trk-proxy.log')
# fh.setFormatter(logging.Formatter(fmt))
# logger.addHandler(ch)
# logger.addHandler(fh)


class Proxy(threading.Thread):
    # subscription
    MANAGER_UPLINK_FORWARD_TOPIC = "manager/uplink/response"  # manager回复设备信息或执行结果到client
    GET_MANAGER_UPLINK_FORWARD_TOPIC = MANAGER_UPLINK_FORWARD_TOPIC + "/#"
    # publish
    MANAGER_DOWNLINK_CMD_TOPIC = "client/downlink/command"  # client获取设备信息或向设备发送指令

    def __init__(self, host, port):
        super(Proxy, self).__init__()
        self.mc = None
        self.host = host
        self.port = port

    def on_connect(self, client, userdata, flags_dict, result):
        # logger.info('proxy connected')
        print("Connected with result code " + str(result))
        client.subscribe(Proxy.GET_MANAGER_UPLINK_FORWARD_TOPIC)
        client.subscribe("chat")

    def on_message(self, client, userdata, message):
        # logger.info('get unknown message:{}'.format(message))
        print(message.topic + " " + ":" + str(message.payload.decode("utf-8")))
        pass

    def on_disconnect(self, client, userdata, result):
        # logger.info('proxy disconnected')
        self.mc = None

    def message_publish(self, topic, payload, **kwargs):
        try:
            if isinstance(payload, dict):
                msg = json.dumps(payload)
            else:
                msg = payload

            assert isinstance(msg, (str, bytes, int, float)) or msg is None
            assert isinstance(topic, str) and topic
            self.mc.publish(topic, msg, **kwargs)
        except Exception as e:
            # logger.error(e)
            pass

    def on_manage_info(self, client, userdata, msg):
        print("收到manage 消息")
        print(msg.topic + " " + ":" + str(msg.payload.decode("utf-8"))+"处理")

    def run(self):

        while True:

            if self.mc is not None:
                time.sleep(0.1)
                continue

            try:
                # logger.info('connect to mqtt...')
                self.mc = mqtt_client.Client()
                self.mc.on_connect = self.on_connect
                self.mc.message_callback_add(Proxy.GET_MANAGER_UPLINK_FORWARD_TOPIC, self.on_manage_info) ## 定义了回调的去执行对应的回调函数,如果没有指明回调函数的的就去调用on_message函数
                # self.mc.message_callback_add("chat", self.on_manage_info)
                self.mc.on_message = self.on_message
                self.mc.on_disconnect = self.on_disconnect
                self.mc.connect(self.host, self.port)
                self.mc.loop_start()
            except Exception as e:
                # logger.error(e)
                # logger.error('proxy connect to mqtt failed!')
                self.mc = None
                time.sleep(3)


# if __name__ == '__main__':
#
#     try:
#         mqtt_host = socket.gethostbyname('trk_mqtt_broker')
#     except:
#         mqtt_host = 'localhost'
#
#     if 'trk_mqtt_broker' in os.environ and os.environ['trk_mqtt_broker']:
#         mqtt_host = os.environ['trk_mqtt_broker']

# p = Proxy(mqtt_host, 1883)
# p = Proxy('127.0.0.1', 1883)
# p.start()
p = Proxy('127.0.0.1', 1883)
p.start()
