#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 版本说明pika==0.10.0

import pika
import json

queue = 'oss.url_test'  # 队列名
routing_key = 'url_test'
exchange = 'oss_test'

# 新建连接，rabbitmq安装在本地则hostname为'localhost'
hostname = '10.6.3.14'
# hostname = '192.168.211.130'
port = 5672
# 1.获得连接对象
credentials = pika.PlainCredentials(username='mq_user', password='password')
parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host='wolong', credentials=credentials)
connection = pika.BlockingConnection(parameters=parameters)

# 2.创建通道
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)  # 创建broker
# 创建任务队列
channel.queue_declare(queue=queue, durable=True)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行

channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)  # 把队列和中间人绑定

data = {"hello": "world"}
# 发送任务
channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(
    data))  # 交换机; 队列名,写明将消息发往哪个队列; 消息内容 # routing_key在使用匿名交换机的时候才需要指定，表示发送到哪个队列,注意当未定义exchange时，routing_key需和queue的值保持一致

# 关闭连接
connection.close()
