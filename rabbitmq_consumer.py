import json
import logging
import pika

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fpcmes.settings")

import django

django.setup()

from django.conf import settings
from mes.device_interface.interfaces import sn_notify
from mes.workshop.device.device_alarm.interfaces import create_device_alarm_record
from mes.workshop.device.device_data.interfaces import create_device_data
from mes.workshop.device.device_running_state.interfaces import create_device_running_state
from mes.onsite_process.inspection.in_and_out_qr_scan.interfaces import multiple_in_and_out_qr_scan
from mes.production.workstation_task.models import WorkstationTask

logger = logging.getLogger(settings.ELK_APP_NAME)

credentials = pika.PlainCredentials(settings.LOCAL_RABBIT_MQ_USERNAME, settings.LOCAL_RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.LOCAL_RABBIT_MQ_HOST, settings.LOCAL_RABBIT_MQ_PORT,
                                       settings.LOCAL_RABBIT_MQ_VHOST,
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='dev2mes_exchange',
                         exchange_type='direct', durable=True)

# result = channel.queue_declare(exclusive=True, durable=True, queue='fpcmes_queue')
result = channel.queue_declare(durable=True, queue='fpcmes_queue')

queue_name = result.method.queue

channel.queue_bind(exchange='dev2mes_exchange',
                   queue=queue_name, routing_key='sn_notify')
channel.queue_bind(exchange='dev2mes_exchange',
                   queue=queue_name, routing_key='qr_code_notify')
channel.queue_bind(exchange='dev2mes_exchange',
                   queue=queue_name, routing_key='report_data')
channel.queue_bind(exchange='dev2mes_exchange',
                   queue=queue_name, routing_key='alarm_report')
channel.queue_bind(exchange='dev2mes_exchange',
                   queue=queue_name, routing_key='device_state')

logger.debug(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    body_str = body.decode()
    body_dict = json.loads(body_str)
    if method.routing_key == 'qr_code_notify':  # 二维码上报
        """
        {
            "device_id": "",    //工控机SN
            "version": "V01",
            "payload":{
                        “cam_id”: "",    //相机ID
                        "sn_list": [         // 序列号列表
                                        {"sn": "",        //序列号
                                        “state”: 0,      //处理状态，0表示成功，1表示失败
                                        “error”: "",     //错误信息
                                        },
                                        {"sn": "",        //序列号
                                        “state”: 0,      //处理状态，0表示成功，1表示失败
                                        “error”: "",     //错误信息
                                        },
                                    ]
                        }
        }
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug('Receive a qr_code_notify type message. data: {}'.format(body_dict))

        multiple_in_and_out_qr_scan(body_dict)

    elif method.routing_key == 'sn_notify':  # 打标机二维码上报
        """
        {
            "device_id": "A3C2POSTestCY001“,        // 设备ID
            "version": "V01",
            “payload”:{
                “line”:”A3C2”,
                ”station”:”POSTest”,
                ”fixture”:”CY001”,
                “sn”:”any”,
                “state”: 0,
                "error_info":''
                }
        }
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 处理成功通知mq、 与no_ack=False 联合使用
        logger.debug('Receive a sn_notify message. data: {}'.format(body_dict))

        sn_notify(body_dict)

    elif method.routing_key == 'report_data':  # 设备数据上报
        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.debug('Receive a report_data message. data: {}'.format(body_dict))

        create_device_data(body_dict)

    elif method.routing_key == 'alarm_report':  # 设备告警上报
        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.debug('Receive a alarm_report message. data: {}'.format(body_dict))

        create_device_alarm_record(body_dict)

    elif method.routing_key == 'device_state':  # 设备告警上报
        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.debug('Receive a device_state message. data: {}'.format(body_dict))

        create_device_running_state(body_dict)

    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error('Receive a not expect routing_key, data: {}'.format(body_dict))


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)

channel.start_consuming()
