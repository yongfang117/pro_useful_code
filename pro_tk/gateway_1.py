# coding:utf-8

import tkinter
from tkinter import *
from tkinter import ttk
import os
import tkinter.filedialog

# import xlrd
# import xlwt

APP_WINDOW = '600x400+200+200'
APP_TITLE = '网关控制小程序'
APP_LOGO = 'cy-logo.ico'


class MyAPP(tkinter.Frame):
    @classmethod
    def logout(cls, logstr=''):
        cls.loghandler.insert(tkinter.END, '\n{}'.format(logstr))
        # 此处可以增加判断鼠标焦点是否在文档的最末尾，如果在最末尾或者无焦点则将执行yview_moveto
        # 否则不执行，这样做是为了便于阅读log
        cls.loghandler.yview_moveto(1)

    def _save(self):
        print(self.entry_ip_val.get(), self.entry_port_val.get())

    def _ctrl(self, *args):  # 处理事件，*args表示可变参数
        # print(self.comboxlist.get())  # 打印选中的值
        if self.comboxlist.get() == "启动":
            print("启动")
        if self.comboxlist.get() == "停止":
            print("停止")
        if self.comboxlist.get() == "重启":
            print("重启")

        if self.dev_list.get() and self.comboxlist.get() and self.module_list.get():
            self.btn_convert.config(state=tkinter.NORMAL)

    def _dev(self, *args):
        print(self.dev_list.get())
        if self.dev_list.get() and self.comboxlist.get() and self.module_list.get():
            self.btn_convert.config(state=tkinter.NORMAL)

    def _module(self, *args):
        print(self.module_list.get())
        if self.dev_list.get() and self.comboxlist.get() and self.module_list.get():
            self.btn_convert.config(state=tkinter.NORMAL)

    def _execute(self):
        print("zhixing")

    def __init__(self):
        self.app = tkinter.Tk()
        tkinter.Frame.__init__(self, master=self.app)
        self.app.geometry(APP_WINDOW)
        self.app.title(APP_TITLE)
        self.app.iconbitmap(APP_LOGO)
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
        # self.btn_input = tkinter.Button(self.app, text='选择输入', command=self._choose_input)
        # self.btn_input.place(x=400, y = 10, height=20)
        # self.btn_input.config(state=tkinter.NORMAL)

        self.btn_save = tkinter.Button(self.app, text='保存', command=self._save)
        self.btn_save.place(x=420, y=15, width=60)
        # self.btn_save.config(state=tkinter.DISABLED)
        self.btn_save.config(state=tkinter.NORMAL)

        self.btn_convert = tkinter.Button(self.app, text='执行', command=self._execute)
        self.btn_convert.place(x=480, y=65, width=60)
        self.btn_convert.config(state=tkinter.DISABLED)

        # 下拉列表
        # 设备下拉列表
        self.dev_value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.dev_list = tkinter.ttk.Combobox(self.app, textvariable=self.dev_value)  # 初始化
        self.dev_list["values"] = ("Dev1", "Dev2", "Dev3")
        self.dev_list.place(x=80, y=70, width=80)
        # comboxlist.current(0)  # 选择第一个
        self.dev_list.bind("<<ComboboxSelected>>", self._dev)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)

        # 指令下拉列表
        self.comvalue = tkinter.StringVar()
        self.comboxlist = tkinter.ttk.Combobox(self.app, textvariable=self.comvalue)
        self.comboxlist["values"] = ("启动", "停止", "重启")
        self.comboxlist.place(x=230, y=70, width=80)
        # comboxlist.current(0)  # 选择第一个
        self.comboxlist.bind("<<ComboboxSelected>>", self._ctrl)  # 绑定事件,

        # 模块下拉列表
        self.module_value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.module_list = tkinter.ttk.Combobox(self.app, textvariable=self.module_value)  # 初始化
        self.module_list["values"] = ("模块1", "模块2", "模块3")
        self.module_list.place(x=380, y=70, width=80)
        # comboxlist.current(0)  # 选择第一个
        self.module_list.bind("<<ComboboxSelected>>", self._module)

        # 消息
        self.message_log0 = tkinter.Text(self.app, background='gray', borderwidth=1)
        self.message_log0.place(x=30, y=150, width=558, height=220)

        self.message_log = tkinter.Text(self.app, background='gray', borderwidth=1)
        self.message_log.place(x=30, y=150, width=540, height=220)
        setattr(self.__class__, 'loghandler', self.message_log)

        # 消息框滚动条
        self.scrollbar_msg = tkinter.Scrollbar(self.message_log0)
        self.scrollbar_msg.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # 绑定消息框和scrollbar
        self.message_log['yscrollcommand'] = self.scrollbar_msg.set
        self.scrollbar_msg['command'] = self.message_log.yview


if __name__ == '__main__':
    ap = MyAPP()
    ap.mainloop()
