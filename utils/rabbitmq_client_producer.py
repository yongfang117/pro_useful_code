"""时间: 2019/12/24
 
作者: liyongfang@cyai.com

更改记录:   

重要说明: 
"""
import logging
import os
import sys

from django.conf import settings
import django

from utils import config
from utils.rabbitmq_client import RabbitMQConnection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wol_server.settings")

django.setup()
sys.path.append("..")
sys.path.append(".")

logger = logging.getLogger(settings.ELK_APP_NAME)


def send_msg(msg):
    """send message to RabbitMQ

    Args:
        msg(dict): 需发送的消息

    Returns:

    """
    routing_key = config.ROUTING_KEY
    RabbitMQConnection().rabbitmq_connection_setup()
    # time.sleep(20)
    ret = RabbitMQConnection.send_rabbitmq_message(msg, routing_key, durable=True)
    logger.info("send message to RabbitMQ result is: {}".format(ret))


if __name__ == '__main__':
    MSG = {"command": 11, "data": "gongxu1"}
    send_msg(MSG)
