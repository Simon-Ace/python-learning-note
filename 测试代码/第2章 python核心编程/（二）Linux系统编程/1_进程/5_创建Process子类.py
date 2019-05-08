'''
创建Process子类，实现run()方法，执行原来target参数的作用
'''

import time
from multiprocessing import Process

class ProcessClass(Process):
    def run(self):
        while True:
            print("----test----")
            time.sleep(1)

p = ProcessClass()
p.start()

