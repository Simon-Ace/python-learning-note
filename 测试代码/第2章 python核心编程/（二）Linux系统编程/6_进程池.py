'''
当进程数很多时，可通过进程池Pool来创建进程
'''

import os
import time
from multiprocessing import Pool

def worker(num):
    for i in range(4):
        print("====pid-%d===num-%d===" % (os.getpid(), num))
        time.sleep(2)

# 创建进程池，参数为进程的最大数量
po = Pool(3)

for i in range(10):
    print("----%d----" % i)
    # 向进程池中添加任务，若任务数超过最大数量则等待
    # 添加任务时不需要等待，直接都放到“等待队列”中
    po.apply_async(worker, (i,))    # apply_async是非堵塞的方式

po.close()  #关闭进程池，即不能再添加新的任务
po.join()   #主进程不会等待进程池结束才结束，因此需要join阻塞住主进程。注意：join之前必须加close