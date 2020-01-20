import threading
import time

lock = threading.Lock()


def get_value(index):
    lock.acquire()
    print(threading.current_thread())
    my_list = [2, 3, 5, 6, 7]
    if index >= len(my_list):
        print("下标越界:", index)
        # 当下标越界需要释放锁，让后面的线程还可以取值
        lock.release()
        return
    print(my_list[index])
    time.sleep(0.2)
    lock.release()


if __name__ == '__main__':
    # 模拟大量线程去执行取值操作
    for i in range(30):
        sub_thread = threading.Thread(target=get_value, args=(i,))
        sub_thread.start()
