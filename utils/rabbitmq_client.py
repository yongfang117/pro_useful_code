"""时间: 2019/12/24
 
作者: liyongfang@cyai.com

更改记录:   

重要说明: 
"""
import json
import logging
import os
import threading

from django.conf import settings
import django
import pika
from utils import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wol_server.settings")

django.setup()

logger = logging.getLogger(settings.ELK_APP_NAME)

CREDENTIALS = pika.PlainCredentials(config.RABBITMQ_USERNAME, config.RABBITMQ_PASSWORD)
PARAMETERS = pika.ConnectionParameters(config.RABBITMQ_HOST, config.RABBITMQ_PORT, config.RABBITMQ_VHOST,
                                       CREDENTIALS, socket_timeout=3)


class RabbitMQConnection(threading.Thread):
    """定义RabbitMQ连接及消息处理类

    """
    SINGLETON_CLIENT_CONNECTION = None
    SINGLETON_CLIENT_CHANNEL = None
    IN_CONNECT = False  # flag
    LOCK = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)

    @classmethod
    def _reconnect(cls):
        """同步连接RabbitMQ时会存在阻塞（阻塞会导致系统进行线程切换），本函数需要考虑多线程调用时线程安全问题。期望处于连接过程中，
        其他线程不要再进行连接，而是直接抛出异常

        Returns:

        Raises:
            InConnectionException: 连接异常

        """
        with cls.LOCK:
            if not cls.IN_CONNECT and (not cls.SINGLETON_CLIENT_CONNECTION or
                                       cls.SINGLETON_CLIENT_CONNECTION.is_closed or
                                       not cls.SINGLETON_CLIENT_CHANNEL or
                                       cls.SINGLETON_CLIENT_CHANNEL.is_closed):
                cls.IN_CONNECT = True
                dispatch = "do_connect"
            else:
                dispatch = "raise_exception"
        if dispatch == "do_connect":
            try:
                cls.SINGLETON_CLIENT_CONNECTION = pika.BlockingConnection(PARAMETERS)
                cls.SINGLETON_CLIENT_CHANNEL = cls.SINGLETON_CLIENT_CONNECTION.channel()
            finally:
                # 此处仅保证IN_CONNECT一定被设置为False，异常交给外层函数处理
                with cls.LOCK:
                    cls.IN_CONNECT = False
        else:
            raise InConnectionException()

    @classmethod
    def _async_reconnect(cls):
        """相比同步连接RabbitMQ方式，异步连接可以减少连接时由于RabbitMQ本身的不响应，导致连接阻塞过长，进而产生影响系统业务的后果

        Returns:

        Raises:
            InConnectionException: 连接异常

        """
        with cls.LOCK:
            if not cls.IN_CONNECT and (not cls.SINGLETON_CLIENT_CONNECTION or cls.SINGLETON_CLIENT_CONNECTION.is_closed
                                       or not cls.SINGLETON_CLIENT_CHANNEL or cls.SINGLETON_CLIENT_CHANNEL.is_closed):
                cls.IN_CONNECT = True
                dispatch = "do_connect"
            else:
                dispatch = "raise_exception"
        if dispatch == "do_connect":

            def _on_open_callback(*args, **kwargs):
                """connection open callback

                Args:
                    *args (tuple): 不定长参数
                    **kwargs (dict): 不定长参数

                Returns:

                """

                def _on_channel_open(*args, **kwargs):
                    """channel open callback

                    Args:
                        *args (tuple): 不定长参数
                        **kwargs (dict): 不定长参数

                    Returns:

                    """
                    with cls.LOCK:
                        cls.IN_CONNECT = False

                    cls.SINGLETON_CLIENT_CHANNEL.basic_publish(exchange=config.EXCHANGE,
                                                               routing_key=config.ROUTING_KEY,
                                                               body="channel is opening",
                                                               properties=pika.BasicProperties(delivery_mode=2))

                try:
                    cls.SINGLETON_CLIENT_CHANNEL = cls.SINGLETON_CLIENT_CONNECTION.channel(
                        on_open_callback=_on_channel_open)
                except Exception as channel_open_error:
                    logger.error("channel open error: {}".format(str(channel_open_error)))
                    cls._process_execption()  # 释放连接资源
                    with cls.LOCK:
                        cls.IN_CONNECT = False

            def _on_open_error_callback(*args, **kwargs):
                """connection open error callback

                Args:
                    *args (tuple): 不定长参数
                    **kwargs (dict): 不定长参数

                Returns:

                """
                cls._process_execption()
                with cls.LOCK:
                    cls.IN_CONNECT = False

            def _rabbit_ioloop_process(connection):
                """RabbitMQ ioloop

                Args:
                    connection (object):  pika.SelectConnection对象

                Returns:

                """
                try:
                    # ioloop: pika.adapters.base_connection
                    # start: pika.adapters.utils.selector_ioloop_adapter
                    connection.ioloop.start()
                except Exception as rabbit_ioloop_error:
                    logger.error("RabbitMQ ioloop error: {}".format(str(rabbit_ioloop_error)))
                    cls._process_execption()

            try:
                cls.SINGLETON_CLIENT_CONNECTION = pika.SelectConnection(parameters=PARAMETERS,
                                                                        on_open_callback=_on_open_callback,
                                                                        on_open_error_callback=_on_open_error_callback)
                threading.Thread(target=_rabbit_ioloop_process, args=(cls.SINGLETON_CLIENT_CONNECTION,)).start()
            except Exception as async_connect_error:
                logger.error("async connect failed: {}".format(str(async_connect_error)))
                # 开始异步连接失败时，IN_CONNECT设置为False，连接开始后又callback回调函数修改IN_CONNECT
                with cls.LOCK:
                    cls.IN_CONNECT = False
        else:
            raise InConnectionException()

    @classmethod
    def _process_execption(cls):
        """exception process

        Returns:

        """
        try:
            if cls.SINGLETON_CLIENT_CHANNEL:
                cls.SINGLETON_CLIENT_CHANNEL.close()
            if cls.SINGLETON_CLIENT_CONNECTION:
                cls.SINGLETON_CLIENT_CONNECTION.close()
        except Exception as connect_rabbitmq_error:
            logger.error("close rabbitmq connection failed: {}".format(str(connect_rabbitmq_error)))
        finally:
            cls.SINGLETON_CLIENT_CHANNEL = None
            cls.SINGLETON_CLIENT_CONNECTION = None

    def rabbitmq_connection_setup(self):
        """建立RabbitMQ连接

        Returns:

        """
        try:
            # self._async_reconnect()
            self._reconnect()
        except Exception as rabbitmq_connection_setup_error:
            logger.error("RabbitMQ connection setup failed: {}".format(str(rabbitmq_connection_setup_error)))
            self._process_execption()

    @classmethod
    def send_rabbitmq_message(cls, message, routing_key, durable):
        """发送消息到RabbitMQ

        Args:
            message (str):  发送的消息
            routing_key (str):  路由键
            durable (bool):  queue是否持久化，默认False

        Returns:
            tuple: 发送成功返回True,OK，发送失败返回False,描述

        """
        ret = (True, "OK")
        try:
            if not cls.IN_CONNECT and (not cls.SINGLETON_CLIENT_CONNECTION or
                                       cls.SINGLETON_CLIENT_CONNECTION.is_closed or not
                                       cls.SINGLETON_CLIENT_CHANNEL or cls.SINGLETON_CLIENT_CHANNEL.is_closed):
                # cls._async_reconnect()
                cls._reconnect()
            if cls.SINGLETON_CLIENT_CHANNEL:
                if durable:
                    send_properties = pika.BasicProperties(delivery_mode=2)
                else:
                    send_properties = None
                cls.SINGLETON_CLIENT_CHANNEL.basic_publish(exchange=config.EXCHANGE,
                                                           routing_key=routing_key,
                                                           body=json.dumps(message),
                                                           properties=send_properties)
            else:
                ret = (False, "RabbitMQ connection is not ready!")
        except InConnectionException as in_connection_error:
            logger.warning("RabbitMQ connection exception: {}".format(str(in_connection_error)))
        except Exception as other_error:
            logger.error("send msg({}) to RabbitMQ({}) port({}) vhost({}) exchange({}) routing_key({}) failed!".format(
                message, config.RABBITMQ_HOST, config.RABBITMQ_PORT, config.RABBITMQ_VHOST, config.EXCHANGE,
                config.ROUTING_KEY
            ))
            logger.error("Unexpected error occur: {}".format(str(other_error)))
            cls._process_execption()
            ret = (False, "Exception error")

        return ret


class InConnectionException(Exception):
    """定义连接异常类

    """

    def __str__(self):
        """抛异常时的打印函数

        Returns:
            str: 异常信息

        """
        return "The main thread is connecting the rabbitmq host."
