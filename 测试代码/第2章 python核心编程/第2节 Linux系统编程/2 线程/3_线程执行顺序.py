"""
线程执行顺序 —— 无序
看CPU如何调度
"""
from threading import Thread
from time import sleep

class MyThread(Thread):
    def run(self):
        for i in range(5):
            print("----%s---%d---" % (self.name, i))
            sleep(1)

for k in range(3):
    t = MyThread()
    t.start()
    print("===================")
