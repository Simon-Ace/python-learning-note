"""
线程共享全局变量的问题
问题：两个线程对一个变量同时赋值的时候可能会出现bug
原因解释：a = a+1这其实可以看为两个步骤，①a+1 ②将a+1的值赋给a
"""

from threading import Thread
import time

g_num = 0

def test1():
    global g_num
    for i in range(2000000):
        g_num += 1

    print("---test1---g_num=%d"%g_num)

def test2():
    global g_num
    for i in range(2000000):
        g_num += 1

    print("---test2---g_num=%d"%g_num)

p1 = Thread(target=test1)
p1.start()

#time.sleep(3) #取消屏蔽之后 再次运行程序，结果会不一样

p2 = Thread(target=test2)
p2.start()

print("---g_num=%d---"%g_num)
