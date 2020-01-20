"""Acquisition gateway controller"""
# coding:utf-8
"""采集网关控制器"""
from tkinter import ttk
import datetime
import json
import socket
import threading
import time
import tkinter
import tkinter.filedialog
import uuid

from paho.mqtt import client as mqtt_client

APP_WINDOW = '600x400+200+200'
APP_TITLE = 'Tarek采集设备控制器'
# APP_LOGO = 'cy-logo.ico'
COMMAND_LIST = ["设备启动", "设备停止", "设备重启", "模块启动", "模块停止", "模块重启"]  # 指令列表
# DEVICE_LIST_INFO = {}  # 用于存储获取设备列表时得到的设备错误码等信息
# DEVICE_LIST_INFO["device_list_info"] = None
DEVICES_ERRS_INFO = []  # 用于存储获取设备列表时得到的设备错误码等信息
MESSAGE_DICT = {}
DEVICES_NEW = []  # 存放得到的设备devices
MQTT_RECEIVED_MESSAGE = []  # 存mqtt收到的消息
identifier = str(uuid.uuid4())
# 请求设备列表消息
MESSAGE_DICT["device_request_message"] = {
    "command": "device",
    "data": {},
    "client_sub_id": identifier
}
# 设备启动请求消息
MESSAGE_DICT["device_start_request_message"] = {
    "command": "device_start",
    "data": {},
    "client_sub_id": identifier
}
# 设备停止请求消息
MESSAGE_DICT["device_stop_request_message"] = {
    "command": "device_stop",
    "data": {},
    "client_sub_id": identifier
}
# 模块启动请求消息
MESSAGE_DICT["mod_start_request_message"] = {
    "command": "mod_start",
    "data": {},
    "client_sub_id": identifier
}
# 模块停止请求消息
MESSAGE_DICT["mod_stop_request_message"] = {
    "command": "mod_stop",
    "data": {},
    "client_sub_id": identifier
}

proxy_cond = threading.Condition()


class Proxy(threading.Thread):
    # subscription
    MANAGER_UPLINK_RESP_TOPIC = "manager/uplink/response"  # manager回复设备信息或执行结果到client
    GET_MANAGER_UPLINK_RESP_TOPIC = MANAGER_UPLINK_RESP_TOPIC + "/#"

    # publish
    MANAGER_DOWNLINK_CMD_TOPIC = "client/downlink/command"  # client获取设备信息或向设备发送指令

    def __init__(self, host, port):
        super(Proxy, self).__init__()
        self.mc = None
        self.host = host
        self.port = port

    def on_connect(self, client, userdata, flags_dict, result):
        message_layout_output('proxy connected')
        print("Connected with result code " + str(result))
        client.subscribe(Proxy.GET_MANAGER_UPLINK_RESP_TOPIC)

    # def on_send(self, client, userdata, message, payload):  # ?
    #
    #     topic = Proxy.MANAGER_DOWNLINK_CMD_TOPIC
    #     self.message_publish(topic, payload, qos=0, retain=False)

    # def on_receive(self, client, userdata, message):
    #     MQTT_RECEIVED_MESSAGE.append[message]

    def on_receive(self, client, userdata, message):
        err_no = None
        error_info = None
        module = "mod00"
        try:
            payload = json.loads(message.payload)
            topic = message.topic
            command = payload["command"]

            if command == "device":
                self.on_receive_device_info(client, userdata, message)
            else:
                device_sub_id = topic.rsplit("/", 1)[1]
                dev = get_dev_name(device_sub_id)
                if command in ["device_start", "device_stop"]:
                    err_no = payload["response"]["err_no"]
                    # error_info = return_err_info(dev, err_no)
                    error_info = return_err_info(err_no)
                    message_layout_output(
                        "服务端执行{} {}指令结果:{}".format(dev, command, error_info if error_info else '未知({})'.format(err_no)))

                elif command in ["mod_start", "mod_stop"]:
                    err_no = payload["response"]["err_no"]
                    # error_info = return_err_info(dev, err_no)
                    error_info = return_err_info(err_no)
                    message_layout_output(
                        "服务端执行{} {} {}指令结果:{}".format(dev, module, command,
                                                      error_info if error_info else '未知({})'.format(err_no)))
    #             return (err_no, error_info)  # 重启时需要使用返回结果
        except json.JSONDecodeError as json_decode_error:
            print("json loads error: {}".format(json_decode_error))
        except KeyError as key_error:
            print("message key error: {}".format(key_error))
        except Exception as other_error:
            print("other error: {}".format(other_error))

    def on_receive_device_info(self, client, userdata, message):
        payload = json.loads(message.payload)
        # 更新设备列表下拉选项
        DEVICES_NEW = payload["response"]["devices"]
        print(payload)
        print(DEVICES_NEW, 222)

        # AP.dev_list["values"] = DEVICES_NEW
        # AP.dev_list.config(state=tkinter.NORMAL)

        # 将收到的设备信息进行处理,以提升后续查询效率,然后存储,
        errors_list = payload["response"]["errors"]
        device_info_dict = {}
        for i in errors_list:
            dev_name = i["device_name"]
            err_list = i["errs"]
            no_info_dict = {}
            for ii in err_list:
                err_no = ii["err_no"]
                err_info = ii["err_info"]
                no_info_dict[err_no] = err_info
            device_info_dict[dev_name] = no_info_dict
            DEVICES_ERRS_INFO = device_info_dict
        print(DEVICES_ERRS_INFO, 333)

    def on_message(self, client, userdata, message):
        # logger.info('get unknown message:{}'.format(message))
        print(message.topic + " " + ":" + str(message.payload.decode("utf-8")))

    def on_disconnect(self, client, userdata, result):
        # logger.info('proxy disconnected')
        message_layout_output('proxy disconnected')
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
            message_layout_output(e)

    def on_manage_info(self, client, userdata, msg):
        print("收到manage 消息")
        print(msg.topic + " " + ":" + str(msg.payload.decode("utf-8")) + "处理")

    def run(self):
        print('in run')
        while True:
            if self.mc is not None:
                time.sleep(0.1)
                continue

            try:
                print('connect to mqtt...')
                # MyAPP.logout('connect to mqtt...') # 阻塞
                message_layout_output('connect to mqtt...')
                self.mc = mqtt_client.Client()
                self.mc.on_connect = self.on_connect
                self.mc.message_callback_add(Proxy.GET_MANAGER_UPLINK_RESP_TOPIC, self.on_receive)
                self.mc.on_message = self.on_message
                self.mc.on_disconnect = self.on_disconnect
                self.mc.connect(self.host, self.port)
                self.mc.loop_start()
                print('init mc loop start')
            except Exception as e:
                message_layout_output(e)
                message_layout_output('proxy connect to mqtt failed!')
                self.mc = None
                time.sleep(3)


# def get_dev_name(device_sub_id):
#     # 根据设备id获取设备名称
#     # TODO
#     return dev


def return_err_info(device_name, err_no=None):
    """返回设备err_no对应信息.获取设备列表时,会收到每个设备对应的错误码信息,根据错误码 err_no 得到 错误码对应的信息err_info

    Args:
        device_name(str): 设备名称
        err_no(int):错误码

    Returns:
        str:错误码对应信息

    """
    data = DEVICES_ERRS_INFO
    if device_name in data.keys():
        dict = data[device_name]
        if err_no in dict.keys():
            err_info = data[device_name][err_no]
            return err_info
    return '成功' if err_no == 0 else None


msg_lock = threading.Lock()
messages_list = []


def message_layout_output(m):
    with msg_lock:
        messages_list.append(m)


def refresh_layout(app):
    app.after(1000, refresh_layout, app)
    with msg_lock:
        while messages_list:
            m = messages_list.pop(0)
            MyAPP.logout(m)


devices_lock = threading.Lock()

def refresh_devices(app):
    app.after(500, refresh_devices, app)
    with devices_lock:
        # print(DEVICES_NEW,444)
        AP.dev_list["values"] = DEVICES_NEW
        AP.dev_list.config(state=tkinter.NORMAL)

# def on_receive_device_info(payload):
#     # 更新设备列表下拉选项
#     DEVICES_NEW = payload["response"]["devices"]
#     print(payload)
#     print(DEVICES_NEW, 222)
#
#     # AP.dev_list["values"] = DEVICES_NEW
#     # AP.dev_list.config(state=tkinter.NORMAL)
#
#     # 将收到的设备信息进行处理,以提升后续查询效率,然后存储,
#     errors_list = payload["response"]["errors"]
#     device_info_dict = {}
#     for i in errors_list:
#         dev_name = i["device_name"]
#         err_list = i["errs"]
#         no_info_dict = {}
#         for ii in err_list:
#             err_no = ii["err_no"]
#             err_info = ii["err_info"]
#             no_info_dict[err_no] = err_info
#         device_info_dict[dev_name] = no_info_dict
#         DEVICES_ERRS_INFO = device_info_dict
#     print(DEVICES_ERRS_INFO, 333)


# handle_lock = threading.Lock()


# def refresh_handle(app):
#     app.after(500, refresh_handle, app)
#     with handle_lock:
#         module = "mod00"
#         message = MQTT_RECEIVED_MESSAGE.pop(0)
#         err_no = None
#         error_info = None
#         dev = AP.dev_list.get()
#         print(dev,444)
#         try:
#             payload = json.loads(message.payload)
#             topic = message.topic
#             command = payload["command"]
#
#             if command == "device":
#                 on_receive_device_info(payload)
#             else:
#                 device_sub_id = topic.rsplit("/", 1)[1]
#
#                 if command in ["device_start", "device_stop"]:
#                     err_no = payload["response"]["err_no"]
#                     # error_info = return_err_info(dev, err_no)
#                     error_info = return_err_info(err_no)
#                     message_layout_output(
#                         "服务端执行{} {}指令结果:{}".format(dev, command, error_info if error_info else '未知({})'.format(err_no)))
#
#                 elif command in ["mod_start", "mod_stop"]:
#                     err_no = payload["response"]["err_no"]
#                     # error_info = return_err_info(dev, err_no)
#                     error_info = return_err_info(err_no)
#                     message_layout_output(
#                         "服务端执行{} {} {}指令结果:{}".format(dev, module, command,
#                                                       error_info if error_info else '未知({})'.format(err_no)))
#
#         AP.dev_list["values"] = DEVICES_NEW
#         AP.dev_list.config(state=tkinter.NORMAL)


class MyAPP(tkinter.Frame):
    """客户端界面"""

    @classmethod
    def logout(cls, logstr=''):
        """日志输出

        Args:
            logstr(str): 要输出的内容

        Returns:

        """
        cls.loghandler.insert(tkinter.END,
                              '\n{} {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), logstr))
        # 此处可以增加判断鼠标焦点是否在文档的最末尾，如果在最末尾或者无焦点则将执行yview_moveto
        # 否则不执行，这样做是为了便于阅读log
        cls.loghandler.yview_moveto(1)

    def get_module_list(self):
        """获取模块列表

        Returns:

        """
        list3_new = ["mod00"]
        self.module_list["values"] = (list3_new)
        self.module_list.config(state=tkinter.NORMAL)

    def connect(self):
        """建立连接,发送设备列表请求消息

        Returns:

        """
        try:
            # if not self.proxy.is_alive(): #如果线程没有开启
            self.proxy.start()
            while self.proxy.mc is None:  # 线程开启后,mc可能没有立即实例化完成
                time.sleep(0.1)
            # t = threading.Thread(target=refresh_layout)
            # t.start()
            # with proxy_cond:
            #     proxy_cond.wait()
            # if not self.proxy.mc:
            #     time.sleep(3)
            payload = MESSAGE_DICT["device_request_message"]
            topic = Proxy.MANAGER_DOWNLINK_CMD_TOPIC
            self.proxy.message_publish(topic, payload, qos=0, retain=False)
            print(DEVICES_NEW, 111)
            print("发送请求列表信息")

        except ConnectionRefusedError as connecterror:
            self.__class__.logout(connecterror)
            self.__class__.logout("连接失败可能的原因: ip或端口号不正确")
        except Exception as error:
            self.__class__.logout(error)

    def execute_status_update(self):
        """执行按钮状态更新

        Returns:

        """
        if self.commond_list.get() in COMMAND_LIST[0:3]:
            if self.dev_list.get() and self.commond_list.get():
                self.btn_execute.config(state=tkinter.NORMAL)
            else:
                self.btn_execute.config(state=tkinter.DISABLED)
        elif self.commond_list.get() in COMMAND_LIST[3:]:
            if self.dev_list.get() and self.commond_list.get() and self.module_list.get():
                self.btn_execute.config(state=tkinter.NORMAL)
            else:
                self.btn_execute.config(state=tkinter.DISABLED)

    def mod_list_status_update(self):
        """模块列表状态更新

        Returns:

        """
        if self.commond_list.get() in COMMAND_LIST[3:]:
            self.module_list.config(state=tkinter.NORMAL)
        else:
            self.module_list.config(state=tkinter.DISABLED)

    def commond(self, *args):
        """选择指令后,模块列表和执行按钮的状态随之改变

        Args:
            *args(str):指令列表选项

        Returns:

        """
        self.__class__.logout("您选择的指令是:{}".format(self.commond_list.get()))
        self.get_module_list()
        self.mod_list_status_update()
        self.execute_status_update()

    def module(self, *args):
        """选择模块后,执行按钮的状态随之改变

        Args:
            *args(str): 模块列表选项

        Returns:

        """
        self.__class__.logout("您选择的模块是:{}".format(self.module_list.get()))
        self.execute_status_update()

    def _device_start(self, dev):
        """设备启动

        Args:
            dev(str): 设备名称

        Returns:
            tuple:返回错误码以及对应信息

        """
        command = "设备启动"
        self.__class__.logout("发送{}{}指令".format(dev, command))
        MESSAGE_DICT["device_start_request_message"]["data"]["device"] = dev  # 构建消息
        payload = MESSAGE_DICT["device_start_request_message"]
        topic = Proxy.MANAGER_DOWNLINK_CMD_TOPIC
        self.proxy.message_publish(topic, payload, qos=0, retain=False)

    def _device_stop(self, dev):
        """设备停止

        Args:
            dev(str): 设备名称

        Returns:
            tuple:返回错误码以及对应信息

        """
        command = "设备停止"
        self.__class__.logout("发送{}{}指令".format(dev, command))
        MESSAGE_DICT["device_stop_request_message"]["data"]["device"] = dev
        payload = MESSAGE_DICT["device_stop_request_message"]
        topic = Proxy.MANAGER_DOWNLINK_CMD_TOPIC
        self.proxy.message_publish(topic, payload, qos=0, retain=False)

    def _module_start(self, dev, module):
        """模块启动

        Args:
            dev(str): 设备名称
            module(str):模块名称

        Returns:
            tuple:返回错误码以及对应信息

        """
        command = "模块启动"
        self.__class__.logout("发送{}{}{}指令".format(dev, module, command))
        MESSAGE_DICT["mod_start_request_message"]["data"]["device"] = dev
        MESSAGE_DICT["mod_start_request_message"]["data"]["mod"] = module
        payload = MESSAGE_DICT["mod_start_request_message"]
        topic = Proxy.MANAGER_DOWNLINK_CMD_TOPIC
        self.proxy.message_publish(topic, payload, qos=0, retain=False)

    def _module_stop(self, dev, module):
        """模块停止

        Args:
            dev(str): 设备名称
            module(str):模块名称

        Returns:
            tuple:返回错误码以及对应信息

        """
        command = "模块停止"
        self.__class__.logout("发送{}{}{}指令".format(dev, module, command))
        MESSAGE_DICT["mod_stop_request_message"]["data"]["device"] = dev
        MESSAGE_DICT["mod_stop_request_message"]["data"]["mod"] = module
        payload = MESSAGE_DICT["mod_stop_request_message"]
        topic = Proxy.MANAGER_DOWNLINK_CMD_TOPIC
        self.proxy.message_publish(topic, payload, qos=0, retain=False)

    def execute(self):
        """根据不同指令,执行对应操作

        Returns:

        """
        dev = self.dev_list.get()
        command = self.commond_list.get()
        module = self.module_list.get()
        if command == "设备启动":
            self._device_start(dev)

        elif command == "设备停止":
            self._device_stop(dev)

        elif command == "设备重启":
            self._device_stop(dev)
            self._device_start(dev)

        elif command == "模块启动":
            self._module_start(dev, module)

        elif command == "模块停止":
            self._module_stop(dev, module)

        elif command == "模块重启":
            self._module_stop(dev, module)
            self._module_start(dev, module)
        else:
            self.__class__.logout("指令未定义")

        self.mod_list_status_update()

    def __init__(self):
        self.app = tkinter.Tk()
        tkinter.Frame.__init__(self, master=self.app)
        self.app.geometry(APP_WINDOW)
        self.app.title(APP_TITLE)
        # self.app.iconbitmap(APP_LOGO)
        self.web_t = None
        self.app.after(1000, refresh_layout, self.app)
        self.app.after(500, refresh_devices, self.app)
        # self.app.after(500, refresh_handle, self.app)

        # 标签
        self.ip = tkinter.Label(self.app, text='ip地址:')
        self.ip.config(font='Helvetica -15 bold', fg='blue')
        self.ip.place(x=50, y=30, anchor="center")

        self.port = tkinter.Label(self.app, text='端口号:')
        self.port.config(font='Helvetica -15 bold', fg='blue')
        self.port.place(x=280, y=30, anchor="center")

        self.device = tkinter.Label(self.app, text='设备:')
        self.device.config(font='Helvetica -15 bold', fg='blue')
        self.device.place(x=50, y=80, anchor="center")

        self.command = tkinter.Label(self.app, text='指令:')
        self.command.config(font='Helvetica -15 bold', fg='blue')
        self.command.place(x=200, y=80, anchor="center")

        self.command = tkinter.Label(self.app, text='模块:')
        self.command.config(font='Helvetica -15 bold', fg='blue')
        self.command.place(x=350, y=80, anchor="center")

        # 输入框
        self.entry_ip_val = tkinter.StringVar()
        # self.entry_ip_val.set("10.6.3.29")
        self.entry_ip_val.set("ec2-54-222-255-109.cn-north-1.compute.amazonaws.com.cn")
        self.entry_ip = tkinter.Entry(self.app, textvariable=self.entry_ip_val)
        self.entry_ip.place(x=90, y=20, width=150)
        self.entry_ip.config(state=tkinter.DISABLED)

        self.entry_port_val = tkinter.StringVar()
        self.entry_port_val.set(1884)
        self.entry_port = tkinter.Entry(self.app, textvariable=self.entry_port_val)
        self.entry_port.place(x=320, y=20, width=80)
        self.entry_port.config(state=tkinter.DISABLED)

        # proxy
        self.proxy = None

        # 按钮
        self.btn_connect = tkinter.Button(self.app, text='连接', command=self.connect)
        self.btn_connect.place(x=420, y=15, width=60)
        self.btn_connect.config(state=tkinter.NORMAL)

        self.btn_execute = tkinter.Button(self.app, text='执行', command=self.execute)
        self.btn_execute.place(x=480, y=65, width=60)
        self.btn_execute.config(state=tkinter.DISABLED)
        # 下拉列表

        # 设备下拉列表
        self.dev_value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.dev_list = ttk.Combobox(self.app, textvariable=self.dev_value)  # 初始化
        list1 = []
        self.dev_list["values"] = (list1)
        self.dev_list.place(x=80, y=70, width=80)
        # comboxlist.current(0)  # 选择第一个
        # self.dev_list.bind("<<ComboboxSelected>>", self.dev)  # 绑定事件
        self.dev_list.config(state=tkinter.DISABLED)  # 初始化时设备不可选

        # 指令下拉列表
        self.commond_value = tkinter.StringVar()
        self.commond_list = ttk.Combobox(self.app, textvariable=self.commond_value)
        self.commond_list["values"] = COMMAND_LIST
        self.commond_list.place(x=230, y=70, width=80)
        self.commond_list.bind("<<ComboboxSelected>>", self.commond)

        # 模块下拉列表
        self.module_value = tkinter.StringVar()
        self.module_list = ttk.Combobox(self.app, textvariable=self.module_value)  # 初始化
        list3 = []
        self.module_list["values"] = (list3)
        self.module_list.place(x=380, y=70, width=80)
        self.module_list.bind("<<ComboboxSelected>>", self.module)
        self.module_list.config(state=tkinter.DISABLED)  # 初始化时模块不可选

        # 消息
        self.message_log0 = tkinter.Text(self.app, background='#FFFFFF', borderwidth=1)
        self.message_log0.place(x=30, y=150, width=558, height=220)

        self.message_log = tkinter.Text(self.app, background='#FFFFFF', borderwidth=1)
        self.message_log.place(x=30, y=150, width=540, height=220)
        setattr(self.__class__, 'loghandler', self.message_log)

        # 消息框滚动条
        self.scrollbar_msg = tkinter.Scrollbar(self.message_log0)
        self.scrollbar_msg.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # 绑定消息框和scrollbar
        self.message_log['yscrollcommand'] = self.scrollbar_msg.set
        self.scrollbar_msg['command'] = self.message_log.yview


if __name__ == '__main__':
    AP = MyAPP()
    host = "ec2-54-222-255-109.cn-north-1.compute.amazonaws.com.cn"
    port = 1884
    P = Proxy(host, port)
    AP.proxy = P
    AP.mainloop()
