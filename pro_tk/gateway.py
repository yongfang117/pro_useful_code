
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import xlrd
import xlwt


def go(*args):  # 处理事件，*args表示可变参数
    print(comboxlist.get())  # 打印选中的值



win = tkinter.Tk()  # 构造窗体
win.title('网关控制小程序')  # 顶层窗口名称
win.geometry("500x300+200+20")  # 设置窗口大小
win.resizable(width=True, height=True)  # 设置窗口是否可变，宽不可变，高可变，默认为True

#创建一个标签,文字，背景颜色，字体（颜色，大小），标签的高和宽
label = Label(win,text='输入文字：',font=('宋体',20),bg='black',width=10,height=8)
label.grid(row=0,column=0)

#创建按钮
button = Button(win,text='按钮',command='hello')
button.pack()

# 下拉列表
comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
comboxlist = ttk.Combobox(win, textvariable=comvalue)  # 初始化
comboxlist["values"] = ("启动", "停止", "重启")
# comboxlist.current(0)  # 选择第一个
comboxlist.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
comboxlist.pack()

win.mainloop()