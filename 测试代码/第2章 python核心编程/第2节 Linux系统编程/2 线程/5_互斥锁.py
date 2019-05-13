"""
互斥锁
解决线程共享全局变量，同时赋值时产生的bug
"""

from threading import Thread, Lock

g_num = 0

def test1():
    global g_num
    for i in range(1000000):
        # 这个线程和test2的线程都在抢这个锁，准备对下面的部分进行上锁，如果一方成功上锁，会导致另一方堵塞（休眠），直到开锁重新抢
        mutex.acquire()
        g_num += 1
        mutex.release() #解锁

    print("---test1---g_num=%d"%g_num)

def test2():
    global g_num
    for i in range(1000000):
        mutex.acquire()
        g_num += 1
        mutex.release()

    print("---test2---g_num=%d"%g_num)

# 创建一个互斥锁，默认是开锁的
mutex = Lock()
p1 = Thread(target=test1)
p1.start()

p2 = Thread(target=test2)
p2.start()

print("---g_num=%d---"%g_num)
