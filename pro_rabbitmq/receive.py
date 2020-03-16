#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 版本说明pika==0.10.0
import pika

queue = 'oss.url_test'  # 队列名
routing_key = 'url_test'
exchange = 'oss_test'

hostname = '10.6.3.14'
# hostname = '192.168.211.130'
port = 5672

# 1.获取连接对象
credentials = pika.PlainCredentials(username='mq_user', password='password')
parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host='wolong', credentials=credentials)
connection = pika.BlockingConnection(parameters=parameters)

#2.创建通道。获取channel对象
channel = connection.channel()

# 3.创建消息队列，如果存在则不创建
channel.queue_declare(queue=queue, durable=True)

# 4.定义回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送ack消息

# 设置公平调度
# channel.basic_qos(prefetch_count=1)  # 添加不按顺序分配消息的参数,可有可无

# 5.关联队列、并设置消息中队列处理的函数
# channel.basic_consume(callback, queue=queue, no_ack=False)  # no_ack来标记是否需要发送ack，默认是False，开启状态 pika=0.10.0可以这样
channel.basic_consume(queue, callback, False)  # pika=1.1.0 位置需要这样

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')

# 6.启动并开始处理消息
channel.start_consuming()
