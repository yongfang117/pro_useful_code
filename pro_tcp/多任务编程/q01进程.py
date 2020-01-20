import multiprocessing
import os
import time


# 跳舞任务
def dance():
    print("dance:", os.getpid())  # 获取当前进程的编号
    print("dance:", multiprocessing.current_process())  # 获取当前进程
    print("dance的父进程编号:", os.getppid())  # 获取父进程的编号
    for i in range(5):
        print("跳舞中...")
        time.sleep(0.2)
        # os.kill(os.getpid(), 9)  # 扩展:根据进程编号杀死指定进程


# 唱歌任务
def sing():
    print("sing:", os.getpid())
    print("sing:", multiprocessing.current_process())
    print("sing的父进程编号:", os.getppid())
    for i in range(5):
        print("唱歌中...")
        time.sleep(0.2)


if __name__ == '__main__':
    print("main:", os.getpid())
    print("main:", multiprocessing.current_process())  # 获取当前进程
    # 创建跳舞的子进程
    # group: 表示进程组，目前只能使用None
    # target: 表示执行的目标任务名(函数名、方法名)
    # name: 进程名称, 默认是Process-1, .....
    dance_process = multiprocessing.Process(target=dance, name="myprocess1")
    sing_process = multiprocessing.Process(target=sing)

    dance_process.start()
    dance_process.join()  # 主进程等待添加数据的子进程执行完成以后程序再继续往下执行，读取数据
    sing_process.start()
