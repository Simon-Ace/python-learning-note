"""
使用Thread子类创建线程
将原来target中关联的函数内容，放到run方法中
"""

from threading import Thread
from time import sleep

class MyThread(Thread):
    def run(self):
        for i in range(3):
            print("I'm " + self.name + '@' + str(i))
            sleep(1)

t = MyThread()
t.start()