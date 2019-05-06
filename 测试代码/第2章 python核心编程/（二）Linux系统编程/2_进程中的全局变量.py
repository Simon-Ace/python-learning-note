import os
import time

ret = os.fork()
num = 100

if ret == 0:
    while 1:
        print("---子进程---num: %d" % num)
        num += 1
        time.sleep(1)
else:
    while 1:
        print("---父进程---num: %d" % num)
        num += 1
        time.sleep(1)