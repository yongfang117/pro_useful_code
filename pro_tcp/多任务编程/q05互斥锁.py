"""
lock = threading.Lock() # 创建锁
lock.acquire()# 上锁
...这里编写代码能保证同一时刻只能有一个线程去操作, 对共享数据进行锁定...
lock.release() # 释放锁
"""
# 提示：加上互斥锁，那个线程抢到这个锁我们决定不了，那线程抢到锁那个线程先执行，没有抢到的线程需要等待
# 加上互斥锁多任务瞬间变成单任务，性能会下降，也就是说同一时刻只能有一个线程去执行
"""

    互斥锁的作用就是保证同一时刻只能有一个线程去操作共享数据，保证共享数据不会出现错误问题
    使用互斥锁的好处确保某段关键代码只能由一个线程从头到尾完整地去执行
    使用互斥锁会影响代码的执行效率，多任务改成了单任务执行
    互斥锁如果没有使用好容易出现死锁的情况
"""
import threading

g_num = 0
lock = threading.Lock()  # 创建全局互斥锁


def sum1():
    lock.acquire()  # 上锁
    for i in range(1000000):  # 不加锁时,验证数据错误,当次数足够多时才会显示出错误来,如果数量太少,看不到结果差异
        global g_num
        g_num += 1
    print(g_num)
    lock.release()  # 释放锁


def sum2():
    lock.acquire()
    for i in range(1000000):
        global g_num
        g_num += 1
    print(g_num)
    lock.release()


if __name__ == '__main__':
    sub_thread1 = threading.Thread(target=sum1)
    sub_thread2 = threading.Thread(target=sum2)
    sub_thread1.start()
    sub_thread2.start()

