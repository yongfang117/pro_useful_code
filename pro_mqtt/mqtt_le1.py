# -*- coding: utf-8 -*-
"""
时间: 2019/11/24 16:29
 
作者: lyf

更改记录:   

重要说明: 
"""

# 关键指令:
# # 1.导入包
# import paho.mqtt.client as mqtt
# # 2.创建client对象
# client = mqtt.Client(id)
# # 3.连接
# client.connect(host, post)
# # 4.订阅
# client.subscribe(topic)
# client.on_message=func #接收到信息后的处理函数
# # 5.发布
# client.publish(topic,payload)

import paho.mqtt.client as mqtt
import sys

# host="192.168.45.3"
host="127.0.0.1"
topic_sub = "Question"
topic_pub = "temperature"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_sub)

def on_message(client, userdata, msg):
    print(msg.payload)
    client.publish(topic_pub, "37°")


def main(argv=None):  # argv是sys模块下的方法用于接收命令行传参
    # 声明客户端
    client=mqtt.Client()
    # 连接
    client.connect(host,1883,60)
    # 两个回调函数,用于执行连接成功和接收到信息要做的事
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

# if __name__ == "__main__":
#     sys.exit(main())
main()