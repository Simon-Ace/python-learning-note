'''
阻塞当前进程，直到调用join方法的那个进程执行完，再继续执行当前进程。
有一个可选参数[timeout]，等待时间，超过这个秒数之后继续执行当前（主）进程
'''

import time
import random
from multiprocessing import Process


def fun():
    for i in range(10):
        print("----test1----")
        time.sleep(1)


p = Process(target=fun)
p.start()
p.join(2)   #可选参数[timeout]

while 1:
    print("----main----")
    time.sleep(1)