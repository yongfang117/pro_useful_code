"""Acquisition gateway controller"""
# coding:utf-8
"""采集网关控制器"""
from tkinter import ttk
import datetime
import json
import socket
import tkinter
import tkinter.filedialog

APP_WINDOW = '600x400+200+200'
APP_TITLE = 'Tarek采集网关控制器'
# APP_LOGO = 'cy-logo.ico'
COMMAND_LIST = ["设备启动", "设备停止", "设备重启", "模块启动", "模块停止", "模块重启"]  # 指令列表
DEVICE_LIST_INFO = {}  # 用于存储获取设备列表时得到的设备错误码等信息
DEVICE_LIST_INFO["device_list_info"] = None
MESSAGE_DICT = {}
# 请求设备列表消息
MESSAGE_DICT["device_request_message"] = {
    "command": "device",
    "data": {}
}
# 设备启动请求消息
MESSAGE_DICT["device_start_request_message"] = {
    "command": "device_start",
    "data": {}
}
# 设备停止请求消息
MESSAGE_DICT["device_stop_request_message"] = {
    "command": "device_stop",
    "data": {}
}
# 模块启动请求消息
MESSAGE_DICT["mod_start_request_message"] = {
    "command": "mod_start",
    "data": {}
}
# 模块停止请求消息
MESSAGE_DICT["mod_stop_request_message"] = {
    "command": "mod_stop",
    "data": {}
}


def client(ip, port, request_message):
    """建立socket连接,发送并接收消息

    Args:
        ip(str):ip地址
        port(int):端口号
        request_message(str):发送的消息

    Returns:
         str:接收到的消息

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        # 客户端发送请求消息
        request_msg = "{}\n".format(json.dumps(request_message))
        print("您要发送的指令为: {}".format(json.dumps(request_message)))
        sock.sendall(request_msg.encode("utf-8"))

        # 客户端接收消息
        recv_data = sock.recv(1024)
        recv_content = recv_data.decode("utf-8")
        msg = recv_content.split("\n")[0]
        payload = json.loads(msg)
        print("您收到的回复信息为:{}".format(payload))
        if payload["command"] == "device":
            list1_new = payload["response"]["devices"]
            AP.dev_list["values"] = (list1_new)
            AP.dev_list.config(state=tkinter.NORMAL)
        return payload
    except Exception as othererror:
        print(othererror)
    finally:
        sock.close()


def return_err_info(device_name, err_no=None):
    """返回设备err_no对应信息.获取设备列表时,会收到每个设备对应的错误码信息,根据错误码 err_no 得到 错误码对应的信息err_info

    Args:
        device_name(str): 设备名称
        err_no(int):错误码

    Returns:
        str:错误码对应信息

    """
    data = DEVICE_LIST_INFO["device_list_info"]
    if device_name in data.keys():
        dict = data[device_name]
        if err_no in dict.keys():
            err_info = data[device_name][err_no]
            return err_info
    return '成功' if err_no == 0 else None


def device_start(ip, port, dev):
    """设备启动

    Args:
        ip(str):ip地址
        port(int):端口号
        dev(str): 设备名称

    Returns:
        tuple:返回错误码以及对应信息

    """
    command = "设备启动"
    AP.__class__.logout("发送{}{}指令".format(dev, command))
    MESSAGE_DICT["device_start_request_message"]["data"]["device"] = dev  # 构建消息
    request_message = MESSAGE_DICT["device_start_request_message"]
    payload = client(ip, port, request_message)
    err_no = payload["response"]["err_no"]
    error_info = return_err_info(dev, err_no)
    AP.__class__.logout("服务端执行{} {}指令结果:{}".format(dev, command, error_info if error_info else '未知({})'.format(err_no)))
    return (err_no, error_info)


def device_stop(ip, port, dev):
    """设备停止

    Args:
        ip(str):ip地址
        port(int):端口号
        dev(str): 设备名称

    Returns:
        tuple:返回错误码以及对应信息

    """
    command = "设备停止"
    AP.__class__.logout("发送{}{}指令".format(dev, command))
    MESSAGE_DICT["device_stop_request_message"]["data"]["device"] = dev
    request_message = MESSAGE_DICT["device_stop_request_message"]
    payload = client(ip, port, request_message)
    err_no = payload["response"]["err_no"]
    error_info = return_err_info(dev, err_no)
    AP.__class__.logout("服务端执行{} {}指令结果:{}".format(dev, command, error_info if error_info else '未知({})'.format(err_no)))
    return (err_no, error_info)


def module_start(ip, port, dev, module):
    """模块启动

    Args:
        ip(str):ip地址
        port(int):端口号
        dev(str): 设备名称
        module(str):模块名称

    Returns:
        tuple:返回错误码以及对应信息

    """
    command = "模块启动"
    AP.__class__.logout("发送{}{}{}指令".format(dev, module, command))
    MESSAGE_DICT["mod_start_request_message"]["data"]["device"] = dev
    MESSAGE_DICT["mod_start_request_message"]["data"]["mod"] = module
    request_message = MESSAGE_DICT["mod_start_request_message"]
    payload = client(ip, port, request_message)
    err_no = payload["response"]["err_no"]
    error_info = return_err_info(dev, err_no)
    AP.__class__.logout(
        "服务端执行{} {} {}指令结果:{}".format(dev, module, command, error_info if error_info else '未知({})'.format(err_no)))
    return (err_no, error_info)


def module_stop(ip, port, dev, module):
    """模块停止

    Args:
        ip(str):ip地址
        port(int):端口号
        dev(str): 设备名称
        module(str):模块名称

    Returns:
        tuple:返回错误码以及对应信息

    """
    command = "模块停止"
    AP.__class__.logout("发送{}{}{}指令".format(dev, module, command))
    MESSAGE_DICT["mod_stop_request_message"]["data"]["device"] = dev
    MESSAGE_DICT["mod_stop_request_message"]["data"]["mod"] = module
    request_message = MESSAGE_DICT["mod_stop_request_message"]
    payload = client(ip, port, request_message)
    err_no = payload["response"]["err_no"]
    error_info = return_err_info(dev, err_no)
    AP.__class__.logout(
        "服务端执行{} {} {}指令结果:{}".format(dev, module, command, error_info if error_info else '未知({})'.format(err_no)))
    return (err_no, error_info)


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
        """建立连接

        Returns:

        """
        try:
            ip = self.entry_ip_val.get()
            port = int(self.entry_port_val.get())
            self.__class__.logout("您输入的ip地址是: {}, 端口号是:{}".format(ip, port))
            request_message = MESSAGE_DICT["device_request_message"]
            payload = client(ip, port, request_message)

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
            DEVICE_LIST_INFO["device_list_info"] = device_info_dict
            self.__class__.logout("连接成功")
        except ConnectionRefusedError as connecterror:
            self.__class__.logout(connecterror)
            self.__class__.logout("连接失败可能的原因: ip或端口号输入不正确")
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

    def execute(self):
        """根据不同指令,执行对应操作

        Returns:

        """
        command = self.commond_list.get()
        ip = self.entry_ip_val.get()
        port = int(self.entry_port_val.get())
        dev = self.dev_list.get()
        module = self.module_list.get()
        if command == COMMAND_LIST[0]:
            device_start(ip, port, dev)
        if command == COMMAND_LIST[1]:
            device_stop(ip, port, dev)
        if command == COMMAND_LIST[2]:
            (err_no, error_info) = device_stop(ip, port, dev)
            if err_no == 0:
                device_start(ip, port, dev)
        if command == COMMAND_LIST[3]:
            module_start(ip, port, dev, module)
        if command == COMMAND_LIST[4]:
            module_stop(ip, port, dev, module)
        if command == COMMAND_LIST[5]:
            (err_no, error_info) = module_stop(ip, port, dev, module)
            if err_no == 0:
                module_start(ip, port, dev, module)
        self.mod_list_status_update()

    def __init__(self):
        self.app = tkinter.Tk()
        tkinter.Frame.__init__(self, master=self.app)
        self.app.geometry(APP_WINDOW)
        self.app.title(APP_TITLE)
        # self.app.iconbitmap(APP_LOGO)
        self.web_t = None

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
        self.entry_ip = tkinter.Entry(self.app, textvariable=self.entry_ip_val)
        self.entry_ip.place(x=90, y=20, width=150)

        self.entry_port_val = tkinter.StringVar()
        self.entry_port = tkinter.Entry(self.app, textvariable=self.entry_port_val)
        self.entry_port.place(x=320, y=20, width=80)

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
    AP.mainloop()
