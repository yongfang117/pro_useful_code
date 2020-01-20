"""时间: 2019/12/24
 
作者: liyongfang@cyai.com

更改记录:   

重要说明: 
"""
import json
import logging
import os

from django.conf import settings
import django
import pika

from utils import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wol_server.settings")

django.setup()

logger = logging.getLogger(settings.ELK_APP_NAME)

CREDENTIALS = pika.PlainCredentials(username=config.RABBITMQ_USERNAME, password=config.RABBITMQ_PASSWORD)
PARAMETERS = pika.ConnectionParameters(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT,
                                       virtual_host=config.RABBITMQ_VHOST,
                                       credentials=CREDENTIALS)
CONNECTION = pika.BlockingConnection(parameters=PARAMETERS)

CHANNEL = CONNECTION.channel()

CHANNEL.exchange_declare(exchange=config.EXCHANGE, exchange_type=config.EXCHANGE_TYPE, durable=True)

# result = channel.queue_declare(exclusive=True, durable=True, queue='fpcmes_queue')
RESULT = CHANNEL.queue_declare(durable=True, queue=config.QUEUE)

QUEUE_NAME = RESULT.method.queue

CHANNEL.queue_bind(exchange=config.EXCHANGE,
                   queue=QUEUE_NAME, routing_key=config.ROUTING_KEY)

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
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error('Receive a not expect command, data: {}'.format(body_dict))


CHANNEL.basic_consume(QUEUE_NAME, callback, False)

CHANNEL.start_consuming()
