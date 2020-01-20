import multiprocessing
import time


def task(count):
    for i in range(count):
        print(i)
        time.sleep(0.2)
    else:
        print("任务执行完")  # for...else...


if __name__ == '__main__':
    # sub_process = multiprocessing.Process(target=task, args=(5,))  # args: 以元组的方式给任务传入参数
    sub_process = multiprocessing.Process(target=task, kwargs={"count": 3})  # kwargs: 以字典方式传入参数
    sub_process.start()
