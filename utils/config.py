"""时间: 2019/12/24
 
作者: liyongfang@cyai.com

更改记录:   

重要说明: 
"""
import os

# RabbitMQ configuration
RABBITMQ_HOST = '10.6.3.14'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'mq_user'
RABBITMQ_PASSWORD = 'password'
RABBITMQ_VHOST = 'wolong'

TOPIC = "P1"  # 产线编号

if 'RABBITMQ_HOST' in os.environ and os.environ['RABBITMQ_HOST']:
    RABBITMQ_HOST = os.environ['RABBITMQ_HOST']

if 'RABBITMQ_PORT' in os.environ and os.environ['RABBITMQ_PORT']:
    try:
        RABBITMQ_PORT = int(os.environ['RABBITMQ_PORT'])
    except Exception:
        pass

if 'RABBITMQ_USERNAME' in os.environ and os.environ['RABBITMQ_USERNAME']:
    RABBITMQ_USERNAME = os.environ['RABBITMQ_USERNAME']

if 'RABBITMQ_PASSWORD' in os.environ and os.environ['RABBITMQ_PASSWORD']:
    RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']

if TOPIC in os.environ and os.environ["TOPIC"]:
    TOPIC = os.environ["TOPIC"]

EXCHANGE = "wolong"
EXCHANGE_NAME = "wolcxdp"
EXCHANGE_TYPE = "direct"
ROUTING_KEY = TOPIC
QUEUE = "wol_queue"

# SQLITE_DB_PATH = 'sqlite:///../data/agent.db'
