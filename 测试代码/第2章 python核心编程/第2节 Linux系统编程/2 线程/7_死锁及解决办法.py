"""
是指两个或两个以上的进程或线程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去
如：有两个线程两把锁。线程1锁住A锁，线程2锁住B锁 -> 线程1此时需要B锁住的内容，线程2需要A锁住的内容，互不相让，程序卡死在这里
"""

import threading
import time

class MyThread1(threading.Thread):
    def run(self):
        if mutexA.acquire():
            print(self.name+'----do1---up----')
            time.sleep(1)

            if mutexB.acquire():
                print(self.name+'----do1---down----')
                mutexB.release()
            mutexA.release()

class MyThread2(threading.Thread):
    def run(self):
        if mutexB.acquire():
            print(self.name+'----do2---up----')
            time.sleep(1)
            if mutexA.acquire():
                print(self.name+'----do2---down----')
                mutexA.release()
            mutexB.release()

mutexA = threading.Lock()
mutexB = threading.Lock()

if __name__ == '__main__':
    t1 = MyThread1()
    t2 = MyThread2()
    t1.start()
    t2.start()


# -------------解决办法-------------
"""
尽量避免这种情况
给acquire()函数添加参数
"""
# mutexA.acquire(blocking=True, timeout=-1)
# blocking设为False，则为非阻塞状态，被锁住了就直接跳过；timeout为等待时间

