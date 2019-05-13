"""
生产者与消费者模式
用于模型解耦
注意：导包问题从queue里面导，别和进程里面那个混了
"""

from queue import Queue
from time import sleep
from threading import Thread, current_thread

def producer():
    global que
    count = 0
    while 1:
        if que.qsize() < 1000:
            for i in range(50):
                count += 1
                msg = "%s produced item %d" % (current_thread().name, count)
                que.put(msg)
                print(msg)
        sleep(0.5)

def consumer():
    global que
    while 1:
        if que.qsize() > 100:
            for i in range(5):
                msg = " %s consume %s" % (current_thread().name, que.get())
                print(msg)
        sleep(1)


que = Queue()

for i in range(100):
    que.put("origin item %d" % i)

for i in range(5):
    csm = Thread(target=consumer)
    csm.start()

for i in range(3):
    pdc = Thread(target=producer)
    pdc.start()
