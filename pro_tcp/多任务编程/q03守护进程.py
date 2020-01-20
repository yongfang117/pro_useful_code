import multiprocessing
import time

def task():
    for i in range(10):
        print("任务执行中...")
        time.sleep(0.2)

if __name__ == '__main__':
    sub_process = multiprocessing.Process(target=task)
    # sub_process.daemon = True # 设置守护主进程，主进程退出子进程直接销毁，子进程的生命周期依赖与主进程
    sub_process.start()
    time.sleep(0.5)
    print("over")
    sub_process.terminate()  # 让子进程销毁
    exit()

    # 总结： 主进程会等待所有的子进程执行完成以后程序再退出
    # 如果想要主进程退出子进程销毁，可以设置守护主进程或者在主进程退出之前让子进程销毁