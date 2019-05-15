# 第2章 python核心编程

[TOC]

[这里有所有上课的笔记](https://www.jianshu.com/u/2e46779cd343)

## 一、python核心编程

### 1. 闭包

- 在函数内再定义一个函数，并且这个函数用到了外边函数的变量，那么将「这个函数以及用到的变量」统称为闭包
  - 用到的上一层函数的变量，只能用不能改值，否则要加`nonlocal`关键字

```python
def test_fun(number):
    def test_in(number2):
        print(number + number2)
    return test_in

ret = test_fun(100)
ret(1)
ret(200)
```



### 2. 装饰器

1） <font color=coral>开放封闭原则：</font>已实现功能的代码不被修改，但可以扩展

使用示例：

```python
def w1(func):
    def inner():
        print("----正在验证权限----")
        if True:
            return func()
        else:
            print("----没有权限----")
    return inner

@w1
def f1():
    print("----f1----")

f1()

# 执行原理
f1 = w1(f1)
f1()
```

2） 执行顺序：

- <u>装饰的时候从下往上装饰，调用时从上往下调用</u>
  - 有多个装饰器，在前面的装饰器会先不装饰，等着下面的都装饰好才装饰
  - 注意下面代码中函数和闭包的执行顺序，以及返回值的装饰顺序
- 装饰器执行时间
  - 只要python解释器执行到了这个代码，就会自动的进行装饰，而不是等到调用的时候才装饰的

```python
def makeBold(func):
    print("----①makeBold 正在装饰----")

    def wrapped():
        print("----①makeBold 正在验证----")
        return "<b>" + func() + "</b>"
    return wrapped

def makeItalic(func):
    print("----②makeItalic 正在装饰----")

    def wrapped():
        print("----②makeItalic 正在验证----")
        return "<i>" + func() + "</i>"

    return wrapped

@makeBold
@makeItalic
def get_string():
    print("----print_string 正在执行 ----")
    return "hello world!"

print(get_string())

# ---- 运行结果 ----
----②makeItalic 正在装饰----
----①makeBold 正在装饰----
----①makeBold 正在验证----
----②makeItalic 正在验证----
----print_string 正在执行 ----
<b><i>hello world!</i></b>
```

3） 对带参数的函数进行装饰

- 在装饰器闭包部分要写上对应的参数

```python
def decor(func):
    def decor_in(a, b):
        print("----decorate func----")
        func(a, b)
    return decor_in

@decor
def ori_func(a, b):
    print("----ori_func: %d, %d----" % (a, b))

ori_func(1,2)
```

- 不定长参数

```python
def decor(func):
    def decor_in(*args, **kwargs):
        print("----decorate func----")
        func(*args, **kwargs)
    return decor_in

@decor
def ori_func(a, b):
    print("----ori_func: %d, %d----" % (a, b))

@decor
def ori_func1(a, b, c):
    print("----ori_func1: %d, %d, %d----" % (a, b, c))

ori_func(1,2)
ori_func1(3, 4, 5)
```

4） 带返回值的函数

- 装饰器内添加return语句

```python
def decor(func):
    def decor_in(*args, **kwargs):
        print("----decorate func----")
        sum = func(*args, **kwargs)
        return sum
    return decor_in

@decor
def ori_func(a, b):
    print("----ori_func: %d, %d----" % (a, b))
    return a + b

sum = ori_func(1,2)
print(sum)
```

5）通用装饰器

```python
def decor(func):
    def decor_in(*args, **kwargs):
        print("----log日志----")
        ret = func(*args, **kwargs)
        return ret
    return decor_in
```

6）带参数的装饰器

- 可以用于在运行时根据参数起不同的装饰作用

```python
def decor_arg(arg):
    def decor(func):
        def decor_in():
            print("----log日志----")
            if arg == "haha":
                func()
                func()
            else:
                func()
        return decor_in
    return decor

@decor_arg("haha")
def ori_fun1():
    print("测试函数1")

@decor_arg("heihei")
def ori_fun2():
    print("测试函数2")

ori_fun1()
ori_fun2()
```

### 3. 生成器

- 基本用法

```python
# 斐波那契数列
def creatNum():
    a, b = 0, 1
    for i in range(10):
        yield b
        a, b = b, a+b

a = creatNum()
for i in a:
    print(i)
```

- send 用法
  - 可作为yield的返回值
  - 但要注意：不可作为第一次迭代时使用，或者用`a.send(None)`

```python
def test_fun():
    i = 0
    while i < 5:
        temp = yield i
        print(temp)
        i += 1

a = test_fun()
print(next(a))
a.send("haha")
```





### 4. 小知识点

（1）模块循环导入：

要避免这种情况，用一个主模块来调用各种子模块

（2）\=\= 和 is：

`==`判断值是否相等  
`is`判断是否指向同一个对象

（3）深拷贝、浅拷贝

深拷贝：把值也拷贝了一份  
浅拷贝：只是多了一个引用

```python
a = [11,22,33]
b = a #浅拷贝
import copy
c = copy.deepcopy(a) #深拷贝，拷贝到最深层的值
d = copy.copy(a) #只拷贝一层，（感觉不会用）
```

（4）私有化

模块中，变量以`_`开头（无论有几个），`from somemodule import *`之后这个变量是不能用的，`import somemodule;   somemodule._xx`就可以用

类中的私有属性：

python中其实是个假private类型，私有属性的名字重整为`_Class__object`

（5）获取模块查找路径

```python
import sys
sys.path

# 添加路径
sys.path.append("path-to-your-file")
```

（5）属性 property

目的是把私有属性变成一般属性，不再调用getter和setter方法

```python
class Test(object):
    def __init__(self):
        self.__num = 100
        
    def setNum(self, newNum):
        print("----setter----")
        self.__num = newNum
        
    def getNum(self):
        print("----getter----")
    	return self.__num
    
    num = property(getNum, setNum)
    
t = Test()
t.num = 100
print(t.num)
```

另一种写法——装饰器

```python
# 两个函数名和调用时的属性名要一致
class Test(object):
    def __init__(self):
        self.__num = 100
        
    @property
    def num(self):
        print("----getter----")
    	return self.__num
    
    @num.setter
    def num(self, newNum):
        print("----setter----")
        self.__num = newNum
        
t = Test()
t.num = 100
print(t.num)
```

（6）作用域

查找符号对应对象的顺序：LEGB

`locals -> enclosing function -> globals -> builtins`

（7）给实例对象添加方法

```python
def eat(self):
    print("----%s在吃----" % self.name)

p1 = Person()
p1.eat = types.MethodType(eat, p1) #前面写p1.eat只是为了方便辨认，其实可以随便写，这里已经把p1当做第一个参数传给eat了，返回的是一个函数指针
```

（8）限制类能添加的属性

```python
class Person(Object):
    __slots__ = ("name", "age")
```



## 二、Linux系统编程

[进程与线程的一个简单解释 - 阮一峰的网络日志](http://www.ruanyifeng.com/blog/2013/04/processes_and_threads.html)

### 1 进程

并发：看上去一起执行（任务数量 > 核数）  
并行：真正一起执行

#### （1）fork创建子进程

- `os.fork()`不能再windows系统上用
- child（子）进程接收返回值为0，而父进程接收子进程的pid作为返回值
- `os.getpid()`获取当前进程的id号 （PID, Process Identification）
- `os.getppid()` 获取父进程id号
- 主进程不会等待子进程的结束

```python
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
        
# -------------OUTPUT--------------
'''
ret: 9298
----父进程----pid:9286
ret: 0
----子进程----pid:9298, ppid:9286
----父进程----pid:9286
'''
```

#### （2）全局变量在多个进程中不共享

- 相当于是有一整份完整的新代码

```python
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
        
# ---------OUTPUT---------
'''
---父进程---num: 100
---子进程---num: 100
---父进程---num: 101
---子进程---num: 101
---父进程---num: 102
---子进程---num: 102
'''
```

#### （3）fork炸弹

```python
#永远不要写下面这种代码！
while True:
    os.fork()
```

#### （4）使用Process创建进程

- 由于`os.fork()`只能用在类unix的系统中，在windows下不能用，因此换用一个更通用的模块
- 主进程会等待子进程的结束

```python
import time
from multiprocessing import Process

def test_fun():
    while 1:
        print("----test1----")
        time.sleep(1)

p = Process(target=test_fun)	#这块注意！只填方法名，不加小括号
# p = Process(target=test_fun, args=('haha',))	#函数有参数时，放在args中。注意：若只有一个												参数，后面加逗号，表示args可迭代
p.start()

while 1:
    print("----main----")
    time.sleep(1)
    
# ------------OUTPUT--------------
'''
----main----
----test1----
----main----
----test1----
'''
```

#### （5）join()进程阻塞

- 阻塞当前进程，直到调用join方法的那个进程执行完，再继续执行当前进程
- 有一个可选参数[timeout]，等待时间，超过这个秒数之后继续执行当前（主）进程

```python
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
    
# ------------OUTPUT-------------
'''
> 先会阻塞主进程2s，然后再执行主进程
----test1----
----test1----
----test1----
----main----
----test1----
----main----
'''
```

#### （6）Process子类

- 创建Process子类，实现run()方法，执行原来target参数的作用
- 还是使用`start()`来启动进程，里面会自动调用`run()`方法

```python
import time
from multiprocessing import Process

class ProcessClass(Process):
    def run(self):
        while True:
            print("----test----")
            time.sleep(1)

p = ProcessClass()
p.start()
```

#### （7）进程池Pool

- 当进程数很多时，可通过进程池Pool来创建进程
- `Pool()`可指定最大进程数
- 主进程不会等待子进程结束
  - 在主进程中需要使用`join()`阻塞住主进程，防止程序直接退出。且`join`之前必须加`close`
- ==<font color=red>**注意！！！**</font>==`apply_async()`这里也是第一个参数只写函数名，后面再跟参数，别加小括号！

```python
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
    # 添加任务时不需要等待，直接都放到“等待队列”中（非阻塞时）
    po.apply_async(worker, (i,))	# apply_async是非堵塞的方式
    #po.apply(worker, (i,))			# apply是阻塞方式，会停在这，等着这个进程完事再继续走

po.close()  #关闭进程池，即不能再添加新的任务
po.join()   #主进程不会等待进程池结束才结束，因此需要join阻塞住主进程。注意：join之前必须加close
```

#### （8）进程间通信

- 进程间数据传递，可用`multiprocessing.Queue()`
- 常用函数：
  - `Queue([num])`创建队列时可指定最大容积
  - `qsize()`返回当前队列包含信息数量
  - `empty()`队列是否为空
  - `full()`是否为满
  - `get([block=True[, timeout]]`取数据，block指定是否阻塞，即一直停在读取状态，timeout等待时间
  - `get_nowait()`相当Queue.get(False)
  - `put(item,[block[, timeout]])`写数据
  - `put_nowait(item)`
- `Process()`通信

```python
from time import sleep
from multiprocessing import Queue, Process, Pool

def read_from_queue(que:Queue):
    while not que.empty():
        print("---read: %s----" % que.get())
        sleep(1)

def write_to_queue(que:Queue):
    for value in ['A', 'B', 'C']:
        print("----write: %s----" % value)
        que.put(value)
        sleep(1)

que = Queue()
pw = Process(target=write_to_queue, args=(que,))
pr = Process(target=read_from_queue, args=(que,))

if __name__ == '__main__':
    pw.start()
    pw.join()

    pr.start()
    pr.join()
```

- `Pool()`通信
  - 使用`multiprocessing.Manager().Queue()`代替`multiprocessing.Queue()`
  - 必须？放到`__main__()`里面才能用

```python
from multiprocessing import Manager,Pool
import os, time

def reader(q):
    print("reader启动(%s),父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in range(q.qsize()):
        print("reader从Queue获取到消息：%s"%q.get(True))
        time.sleep(1)

def writer(q):
    print("writer启动(%s),父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in "dongGe":
        q.put(i)
        print("写入数据到队列：%s" % i)
        time.sleep(1)

if __name__ == "__main__":
    print("(%s) start" % os.getpid())
    q = Manager().Queue()  # 使用Manager中的Queue来初始化
    po = Pool()
    # 使用阻塞模式创建进程，这样就不需要在reader中使用死循环了，可以让writer完全执行完成后，再用reader去读取
    po.apply(writer,(q,))
    po.apply(reader,(q,))
    po.close()
    po.join()
    print("(%s) End"%os.getpid())
```

#### （9）实战：多进程拷贝文件

- [详见代码](.\测试代码\第2章 python核心编程\（二）Linux系统编程\8_实战-多进程拷贝文件.py)

#### （10）孤儿进程与僵尸进程

[孤儿进程与僵尸进程[总结] - Rabbit_Dale - 博客园](https://www.cnblogs.com/Anker/p/3271773.html)

- 孤儿进程：一个父进程退出，而它的一个或多个子进程还在运行，那么那些子进程将成为孤儿进程。孤儿进程将被init进程(进程号为1)所收养，并由init进程对它们完成状态收集工作。

- 僵尸进程：一个进程使用fork创建子进程，如果子进程退出，而父进程并没有调用wait或waitpid获取子进程的状态信息，那么子进程的进程描述符仍然保存在系统中。这种进程称之为僵尸进程。



### 2 线程

进程是资源分配的单位，线程是CPU调度的单位（是进程里面真正执行代码的东西）

#### （1）Thread创建多线程

```python
from threading import Thread
from time import sleep

def fun():
    print("hahaha")
    sleep(1)

for i in range(5):
    t = Thread(target=fun)
    t.start()
```

#### （2）使用Thread子类创建线程

```python
from threading import Thread
from time import sleep

class MyThread(Thread):
    def run(self):
        for i in range(3):
            print("I'm " + self.name + '@' + str(i))
            sleep(1)

t = MyThread()
t.start()
```

#### （3）线程执行顺序

- 无序，看CPU如何调度

```python
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
```

#### （4）线程共享全局变量的问题

- 对于线程来说只有「一份代码」，不像进程来说相当于有「多份代码」互不干涉
  - 因此对于同一个全局变量，一个线程把它修改之后，另一个线程会获取到修改后的值
  - 把列表当做参数传到函数中也一样，（数值类型不行）
- **问题：**两个线程对一个变量同时赋值的时候可能会出现bug
  - 原因解释：`a = a+1`这其实可以看为两个步骤，①`a+1`②将`a+1`的值赋给`a`

```python
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
# 两个线程执行完毕后，g_num!=4000000

print("---g_num=%d---"%g_num)

# ------------OTUPUT--------------
'''
g_num最后不等于4000000
---g_num=353882---
---test1---g_num=2209395
---test2---g_num=2376780
'''
```

#### （5）解决变量被同时修改的问题 —— 互斥锁

- 方法1（不推荐）：**轮询**
  - 加一个新的全局变量，改之前先判断哪个线程满足，满足的执行，不满足的用个`while True`一直查询着，等上一个执行完再执行
  - 可以解决同时修改的问题，但也把多线程任务变成了“单线程”，且一直查询的过程会消耗GPU资源
- 方法2（推荐）：**互斥锁**
  - 一个线程在用的时候，另一个等待。不同于「轮询」的是，不会一直占着CPU资源，等待的过程中那个线程其实是休眠的
  - 只把不同线程都要修改的地方包起来，范围越小越好
  - 会影响性能，比没加互斥锁的时候慢了很多
  - `threading.Lock()`，获取`lock.acquire()`，释放`lock.release()`
  - 有多个锁的时候怎么搞？？（创建多个`Lock()`实例）

```python
from threading import Thread, Lock

g_num = 0

def test1():
    global g_num
    for i in range(1000000):
        # 这个线程和test2的线程都在抢这个锁，准备对下面的部分进行上锁，如果一方成功上锁，会导致另一方堵塞（休眠），直到开锁重新抢
        mutex.acquire()
        g_num += 1
        mutex.release() #解锁

    print("---test1---g_num=%d"%g_num)

def test2():
    global g_num
    for i in range(1000000):
        mutex.acquire()
        g_num += 1
        mutex.release()

    print("---test2---g_num=%d"%g_num)

# 创建一个互斥锁，默认是开锁的
mutex = Lock()
p1 = Thread(target=test1)
p1.start()

p2 = Thread(target=test2)
p2.start()

print("---g_num=%d---"%g_num)
```

#### （6）多线程使用非共享变量

- 每个线程有一份，互不影响

#### （7）死锁及解决办法

- 是指两个或两个以上的进程或线程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去
- 如：有两个线程两把锁。线程1锁住A锁，线程2锁住B锁 -> 线程1此时需要B锁住的内容，线程2需要A锁住的内容，互不相让，程序卡死在这里

```python
import threading
import time

class MyThread1(threading.Thread):
    def run(self):
        if mutexA.acquire():
            print(self.name+'----do1---up----')
            time.sleep(1)

            if mutexB.acquire():
                print(self.name+'----do1---down----')
                mutexB.release()
            mutexA.release()

class MyThread2(threading.Thread):
    def run(self):
        if mutexB.acquire():
            print(self.name+'----do2---up----')
            time.sleep(1)
            if mutexA.acquire():
                print(self.name+'----do2---down----')
                mutexA.release()
            mutexB.release()

mutexA = threading.Lock()
mutexB = threading.Lock()

if __name__ == '__main__':
    t1 = MyThread1()
    t2 = MyThread2()
    t1.start()
    t2.start()
```

- 解决办法：
  - 尽量避免这种情况
  - 给`acquire()`函数添加参数

```python
acquire(blocking=True, timeout=-1)
# blocking设为False，则为非阻塞状态，被锁住了就直接跳过；timeout为等待时间
'''
Acquire a lock, blocking or non-blocking.

When invoked with the blocking argument set to True (the default), block until the lock is unlocked, then set it to locked and return True.

When invoked with the blocking argument set to False, do not block. If a call with blocking set to True would block, return False immediately; otherwise, set the lock to locked and return True.

When invoked with the floating-point timeout argument set to a positive value, block for at most the number of seconds specified by timeout and as long as the lock cannot be acquired. A timeout argument of -1 specifies an unbounded wait. It is forbidden to specify a timeout when blocking is false.

The return value is True if the lock is acquired successfully, False if not (for example if the timeout expired).
'''
```

#### （8）同步和异步 & 阻塞和非阻塞

- 同步是指「协同步调」按预定的先后次序运行。如：你说完，我再说
- 异步就是「谁先执行不确定」

> [怎样理解阻塞非阻塞与同步异步的区别？ - 愚抄的回答 - 知乎](https://www.zhihu.com/question/19732473/answer/23434554)
>
> 1 老张把水壶放到火上，立等水开。（同步阻塞）
> 老张觉得自己有点傻
> 2 老张把水壶放到火上，去客厅看电视，时不时去厨房看看水开没有。（同步非阻塞）
> 老张还是觉得自己有点傻，于是变高端了，买了把会响笛的那种水壶。水开之后，能大声发出嘀~~~~的噪音。
> 3 老张把响水壶放到火上，立等水开。（异步阻塞）
> 老张觉得这样傻等意义不大
> 4 老张把响水壶放到火上，去客厅看电视，水壶响之前不再去看它了，响了再去拿壶。（异步非阻塞）

#### （9）同步的使用

- 通过互斥锁，来保证执行顺序

```python
from threading import Thread, Lock
from time import sleep

def fun1():
    while True:
        if lock1.acquire():
            print("----task1----")
            sleep(0.5)
            lock2.release()

def fun2():
    while True:
        if lock2.acquire():
            print("----task2----")
            sleep(0.5)
            lock3.release()

def fun3():
    while True:
        if lock3.acquire():
            print("----task3----")
            sleep(0.5)
            lock1.release()

lock1 = Lock()
lock2 = Lock()
lock3 = Lock()

lock2.acquire()
lock3.acquire()

t1 = Thread(target=fun1)
t2 = Thread(target=fun2)
t3 = Thread(target=fun3)

t1.start()
t2.start()
t3.start()
```

#### （10）生产者与消费者模式

- 原因：当有两个线程速度不匹配时，为防止资源浪费，在两个线程之间建立一个缓冲区域「队列」
- 目的：给生产者和消费者解耦
- 注意：导包问题从queue里面导，别和进程里面那个混了

```python
from queue import Queue
from time import sleep
from threading import Thread, current_thread

def producer():
    global que
    count = 0
    while 1:
        if que.qsize() < 1000:
            for i in range(50):
                count += 1
                msg = "%s produced item %d" % (current_thread().name, count)
                que.put(msg)
                print(msg)
        sleep(0.5)

def consumer():
    global que
    while 1:
        if que.qsize() > 100:
            for i in range(5):
                msg = " %s consume %s" % (current_thread().name, que.get())
                print(msg)
        sleep(1)


que = Queue()

for i in range(100):
    que.put("origin item %d" % i)

for i in range(5):
    csm = Thread(target=consumer)
    csm.start()

for i in range(3):
    pdc = Thread(target=producer)
    pdc.start()
```

#### （11）多线程传递参数

- 问题：多线程传递变量时的麻烦
  - 将变量作为参数传到函数中——若参数多的时候太麻烦
  - 将变量改成全局变量——多线程之间又会互相影响
  - 使用全局字典（每个线程作为独特的键进行存储）——麻烦，且不便于理解？
  - **「ThreadLocal」**—— 这个东西创建出来对象的属性，在各个线程之间互不干扰（是同一个属性名也没事）

```python
import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('dongGe',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('老王',), name='Thread-B')
t1.start()
t2.start()
```

#### （12）异步的实现（进程）

- 正在做一件事，但不知道做到什么时候，做事的期间去做另外一件事

```python
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
```

#### （13）GIL问题

[谈谈python的GIL、多线程、多进程 - 知乎](https://zhuanlan.zhihu.com/p/20953544)

- GIL的全称是Global Interpreter Lock（全局解释器锁）
  - python下多线程是鸡肋，推荐使用多进程！
  - python下想要充分利用多核CPU，就用多进程
- 在Python多线程下，每个线程的执行方式：
  - 1.获取GIL
    2.执行代码直到sleep或者是python虚拟机将其挂起。
    3.释放GIL
  - 可见，某个线程想要执行，必须先拿到GIL，我们可以把GIL看作是“通行证”，并且在一个python进程中，GIL只有一个。拿不到通行证的线程，就不允许进入CPU执行
  - 而每次释放GIL锁，线程进行锁竞争、切换线程，会消耗资源。并且由于GIL锁存在，**python里一个进程永远只能同时执行一个线程**(拿到GIL的线程才能执行)，这就是为什么在多核CPU上，python的多线程效率并不高
- GIL设计原因 —— 数据安全
  - 多线程资源共享，意味着数据的安全性遇到挑战，而多个进程之间的数据是独立的
  - 由于多线程的资源共享就不可避免的遇到线程安全问题，即同一时刻，必须保证只有一个线程对共享资源进行修改，加锁就是一种同步机制

#### （14）多线程和多进程

- 由于GIL锁的存在，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核
- Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响

| **对比维度**  | **多进程**  | **多线程**   | **总结** |
| ------------ | ------------ | ------------ | ---------- |
| 数据共享、同步 | 数据共享复杂，需要用IPC；数据是分开的，同步简单              | 因为共享进程数据，数据共享简单，但也是因为这个原因导致同步复杂 | 各有优势 |
| 内存、CPU      | 占用内存多，切换复杂，CPU利用率低  | 占用内存少，切换简单，CPU利用率高  | 线程占优 |
| 创建销毁、切换 | 创建销毁、切换复杂，速度慢  | 创建销毁、切换简单，速度很快| 线程占优 |
| 编程、调试 | 编程简单，调试简单| 编程复杂，调试复杂| 进程占优 |
| 可靠性 | 进程间不会互相影响 | 一个线程挂掉将导致整个进程挂掉| 进程占优 |
| 分布式 | 适应于多核、多机分布式；如果一台机器不够，扩展到多台机器比较简单 | 适应于多核分布式| 进程占优 |

## 三、网络编程

### （一）网络编程概述、SOCKET

#### 1 网络编程概述

##### （1）TCP/IP协议(族)

##### （2）网络结构

- 四层结构：链路层 -> 网络层 -> 传输层 -> 应用层
  - 实际编码的结构
- 七层结构：物理层 -> 数据链路层 ->网络层 -> 传输层 -> 会话层 -> 表示层 -> 应用层
  - 理论上的结构

##### （3）端口

- 用来标记一个进程的东西
  - 类比教室的门口
  - 操作系统收到了一条数据，根据端口号，给到对应的程序上
  - 为啥不用pid标识，多台电脑pid不相同
- 端口分配
  - 知名端口（Well Known Ports）：
    - 0~1023 （自己的程序不可以占用这些端口）
    - `80端口分配给HTTP服务
      21端口分配给FTP服务`
  - 动态端口（Dynamic Ports）：
    - 1024~65535

##### （4）ip地址

- 作用：用来在网络中标记一台电脑的一串数字
- 分类
  - 根据网络地址和主机地址的位数进行分类
  - ![2-3-1-1-4_ip地址分类](https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-1-1-4_ip%E5%9C%B0%E5%9D%80%E5%88%86%E7%B1%BB.png)
  - 前面几位是标志位，标识第几类IP
- 私有IP & 公有IP
  - 公有IP全球可访问
  - 私有IP只能在局域网内访问
- 保留IP
  - 「网络号+最小的主机号」为网络号
  - 「网络号+最大的主机号」为广播地址
  - 如网络号为`192.168.119`，那么`192.168.119.0`为网络号；`192.168.119.255`为广播地址

#### 2 ★socket（套接字）

##### （1）socket简介

- 通过网络使**进程**间通信的方式
- **tcp**慢 稳定 **udp**快 容易丢数据
  - udp类似于写信
    - 每一封信都有收件人的地址
    - 不稳定（信丢了就丢了），但是在局域网中丢包率极低
  - tcp类似于打电话
    - 只有打电话的时候有地址，建立好通路之后，就不需要了
    - 稳定（可重播）

##### （2）创建socket 

在另一台Ubuntu电脑进行监听
`sudo tcpdump udp port 8080 -A`

```python
from socket import *

# AF_INET:用于 Internet 进程间通信; SOCK_STREAM（流式套接字，主要⽤于# TCP 协议）,SOCK_DGRAM（数据报套接字，主要用于 UDP 协议）
udpsocket = socket(AF_INET, SOCK_DGRAM)
# 使用UDP发送数据，每一次都要写上接收方的ip和port
udpsocket.sendto(b"what's that", ('192.168.25.3', 8080))
```

- 每重新运行一次程序端口号都不一样
- 同一个os中不允许两个进程有同一个端口，因为会造成冲突

##### （3）udp绑定信息

- 请求方一般不绑定端口，接收方要绑定，告诉另外一方你监听的接口

```python
from socket import *

udpsocket = socket(AF_INET, SOCK_DGRAM)
udpsocket.bind(("", 7777)) #第一个是ip地址，空表示本机ip

# 发送
# udpsocket.sendto(b"constant port data", ('192.168.25.3', 8080))

# 接收
while 1:
    recv_data = udpsocket.recvfrom(1024)
    print(recv_data)
```

##### （4）单工、半双工、全双工

- 单工
  - 只能收或只能发信息（只具备一项功能，如收音机）
- 半双工
  - 双方都能收发信息，但同一时间只能有一方发信息
- 全双工
  - 可同时收发

##### （5）编码问题

- 前面发送的时候，字符串前面都要加个`b`，使用bytes类型发送
  - 有个问题是，只能编码常用（原始）的asc字符，其他的会乱码
- 指定编解码（注意双方要对应，常用的`utf-8`、`gb2312`）
  - 发送时：`data.encode("utf-8")`
  - 接收时：`content.decode("utf-8")`

##### （6）udp网络通信过程

![2-3-1-2-6 udp网络通信过程](https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-1-2-6%20udp%E7%BD%91%E7%BB%9C%E9%80%9A%E4%BF%A1%E8%BF%87%E7%A8%8B.jpg)

[IP地址和MAC地址的区别和联系是什么？ - neevek的回答 - 知乎](https://www.zhihu.com/question/49335649/answer/120746792)

- 到这里你可能还有疑问，假设没有 IP，只用 MAC 就不能实现这种超远程的互联吗？答案是可以的，但那样会失去很多的灵活性，因为 MAC 是全局唯一的，不存在『MAC 子网』这样的东西，意味着只使用 MAC 没办法创建子网络，全人类只有唯一一个大网络。

##### （7）多线程聊天

[详见代码](.\测试代码\第2章 python核心编程\第3节 网络编程\1 网络编程概述、socket\4_多线程聊天.py)

- 用多线程解决
- print函数改了end参数后，记得加flush让其立马显示