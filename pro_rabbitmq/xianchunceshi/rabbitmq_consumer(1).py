"""时间: 2019/12/24
 
作者: liyongfang@cyai.com

更改记录:   

重要说明: 
"""
import json
import logging
import os

import pika

LINE_NO = os.environ.get('LINE_NO', '2')  # 产线编号

RABBIT_HOST = os.environ.get('RABBIT_HOST', '10.6.3.14')
RABBIT_PORT = int(os.environ.get('RABBIT_PORT', '5672'))
RABBIT_USER = os.environ.get('RABBIT_USER', 'mq_user')
RABBIT_PASS = os.environ.get('RABBIT_PASS', 'password')
RABBIT_VHOST = os.environ.get('RABBIT_VHOST', 'wolong')
RABBIT_EXCHANGE = os.environ.get('RABBIT_EXCHANGE', 'wolong-uplink')
RABBIT_EXCHANGE_TYPE = os.environ.get('RABBIT_EXCHANGE_TYPE', 'direct')
RABBIT_ROUTING_KEY = LINE_NO
QUEUE = "wol_queue"


logger = logging.getLogger("wolong")

CREDENTIALS = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PASS)
PARAMETERS = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT,
                                       virtual_host=RABBIT_VHOST,
                                       credentials=CREDENTIALS)
CONNECTION = pika.BlockingConnection(parameters=PARAMETERS)

CHANNEL = CONNECTION.channel()

CHANNEL.exchange_declare(exchange=RABBIT_EXCHANGE, exchange_type=RABBIT_EXCHANGE_TYPE, durable=True)

# result = channel.queue_declare(exclusive=True, durable=True, queue='fpcmes_queue')
RESULT = CHANNEL.queue_declare(durable=True, queue=QUEUE)

QUEUE_NAME = RESULT.method.queue
print("QUEUE_NAME= ", QUEUE_NAME)

CHANNEL.queue_bind(exchange=RABBIT_EXCHANGE,
                   queue=QUEUE_NAME, routing_key=RABBIT_ROUTING_KEY)

logger.debug(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body, *args, **kwargs):
    """收到消息的回调函数

    Args:
        ch(object): hannel
        method(object): method
        properties(object): properties
        body(object):接收的消息
        *args(tuple):位置参数
        **kwargs(dict):关键字参数

    Returns:

    """
    try:
        body_str = body.decode()
        body_dict = json.loads(body_str)
        logger.info("msg body: {}".format(body_dict))
        handle_message(ch, method, properties, body_dict)
    except json.JSONDecodeError as json_decode_error:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error("json loads error: {}".format(json_decode_error))
    except KeyError as key_error:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error("message key error: {}".format(key_error))
    except AssertionError as assert_error:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error("verify_message error: {}".format(assert_error))
    except Exception as other_error:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error("other error: {}".format(other_error))


def handle_message(ch, method, properties, body_dict, *args, **kwargs):
    """根据接收的消息做对应处理

    Args:
        ch(object): hannel
        method(object): method
        properties(object): properties
        body_dict(object):接收的消息
        *args(tuple):位置参数
        **kwargs(dict):关键字参数

    Returns:

    """
    command = body_dict['command']
    if command == 1:  # 上报喷码数据（spurt_code返回载板号，SN）
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 2:  # 剪针脚
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 3:  # 上报AOI检测数据
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 4:  # 上报压线夹数据
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 5:  # 上报FCT测试结果
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 6:  # 上报下料信息
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 7:  # 上报设备状态
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 8:  # 上报某工位操作员操作时间
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 9:  # 开始工单任务结果
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif command == 10:  # 停止工单任务结果
        print('Receive  message. data: {}'.format(body_dict))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error('Receive a not expect command, data: {}'.format(body_dict))


CHANNEL.basic_consume(QUEUE_NAME, callback, False)

CHANNEL.start_consuming()
