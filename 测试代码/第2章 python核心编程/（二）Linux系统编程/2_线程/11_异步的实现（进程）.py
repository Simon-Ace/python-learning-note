"""
异步的实现

正在做一件事，但不知道做到什么时候，做事的期间去做另外一件事
"""

from multiprocessing import Pool
from time import sleep
import os

def fun():
    print("---进程池中的进程---pid=%d, ppid=%d---" % (os.getpid(), os.getppid()))
    for i in range(3):
        print("---%d---" % i)
        sleep(1)
    return "haha"

# 这个函数是主进程执行的，但是执行的时候主进程在sleep，体现了异步的思想
def fun_callback(args):
    print("---callback func--pid=%d---" % os.getpid())
    print("---callback func--args=%s---" % args)


if __name__ == '__main__':
    pool = Pool(3)

    for i in range(3):
        pool.apply_async(fun, callback=fun_callback)

    pool.close()
    pool.join()

    sleep(5)
    print("---主进程结束---")