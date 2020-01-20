# 设置守护主线程有两种方式：
#
#     threading.Thread(target=show_info, daemon=True)
#     线程对象.setDaemon(True)

import threading
import time


# 带有参数的任务
def task(count):
    for i in range(count):
        print("任务执行中..")
        time.sleep(0.2)
    else:
        print("任务执行完成")


if __name__ == '__main__':
    # print("dance当前执行的线程为：", threading.current_thread()) # 获取线程id

    sub_thread = threading.Thread(target=task, args=(5,), daemon=True)   # args: 以元组的方式给任务传入参数
    # sub_thread = threading.Thread(target=task, kwargs={"count": 3})
    # 设置成为守护主线程，主线程退出后子线程直接销毁不再执行子线程的代码
    # 守护主线程方式2
    # sub_thread.setDaemon(True)
    sub_thread.start()
