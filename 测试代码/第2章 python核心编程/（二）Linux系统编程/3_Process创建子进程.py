'''
由于os.fork()只能用在类unix的系统中，在windows下不能用，因此换用一个更通用的模块
'''
import time
from multiprocessing import Process

def test_fun():
    while 1:
        print("----test1----")
        time.sleep(1)


p = Process(target=test_fun)	#这块注意！只填方法名，不加小括号
# p = Process(target=test_fun, args=('haha',))	#函数有参数时，放在args中。注意：若只有一个参数，后面加逗号，表示args可迭代
p.start()

while 1:
    print("----main----")
    time.sleep(1)