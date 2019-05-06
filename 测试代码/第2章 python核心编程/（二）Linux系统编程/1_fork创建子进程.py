import os
import time

# child（子）进程接收返回值为0，而父进程接收子进程的pid作为返回值
ret = os.fork()
print("ret: %d" % ret)
if ret > 0:
    while 1:
        print("----父进程----pid:%d" % os.getpid())
        time.sleep(1)
else:
    while 1:
        print("----子进程----pid:%d, ppid:%d" % (os.getpid(), os.getppid()))
        time.sleep(1)
