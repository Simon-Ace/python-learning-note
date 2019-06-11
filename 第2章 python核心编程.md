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

#### （1） <font color=coral>开放封闭原则：</font>

已实现功能的代码不被修改，但可以扩展

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

#### （2） 执行顺序：

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

#### （3） 对带参数的函数进行装饰

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

#### （4） 带返回值的函数

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

#### （5）通用装饰器

```python
def decor(func):
    def decor_in(*args, **kwargs):
        print("----log日志----")
        ret = func(*args, **kwargs)
        return ret
    return decor_in
```

#### （6）带参数的装饰器

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

#### （7）* 类做装饰器

「不重要」

1. 当用Test来装作装饰器对test函数进行装饰的时候，首先会创建Test的实例对象并且会把test这个函数名当做参数传递到`__init__`方法中。即在`__init__`用法中的func变量指向了test函数体

2. test函数相当于指向了用Test创建出来的实例对象

3. 当在使用`test()`进行调⽤时，就相当于让这个对象()，因此会调用这个对象的`__call__`方法

4. 为了能够在`__call__`方法中调用原来test指向的函数体，所以在`__init__`方法中就需要一个实例属性来保存这个函数体的引用。所以才有了`self.__func = func`这句代码，从而在调用`__call__`方法中能够调用到test

```python
class Test(object):
	def __init__(self, func):
		print("---初始化---")
		print("func name is %s"%func.__name__)
		self.__func = func
    def __call__(self):
        print("---装饰器中的功能---")
        self.__func()
        
@Test
def test():
   print("----test---")
test()
showpy()#如果把这句话注释，重新运⾏程序，依然会看到"--初始化--"

# ---------------OUTPUT---------------
'''
---初始化---
func name is test
---装饰器中的功能---
----test----
'''
```



### 3. 生成器

#### （1）基本用法

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

#### （2）send 用法

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



### 4. * 元类

「不重要」

#### （1）类也是对象

- 在大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段
- 但是，Python中的类还远不止如此。类同样也是一种对象
  - 类这个对象拥有创建对象（实例对象）的能力。但是，它的本质仍然是一个对象

#### （2）type动态创建类

- 用到的时候再补充



### 5. 垃圾回收GC

#### （1）创建对象原则

- 小整数[-5,257)共用对象，常驻内存
- 大整数不共用内存，引用计数为0，销毁
- 单个字符共用对象，常驻内存
- 单个单词，不可修改，默认开启intern机制，共用对象，引用计数为0，则销毁
- 字符串（含有空格），不可修改，没开启intern机制，不共用对象，引用计数为0，销毁
- 数值类型和字符串类型在 Python 中都是不可变的，这意味着你无法修改这个对象的值，每次对变量的修改，实际上是创建一个新的对象

#### （2）垃圾回收机制

**「采用 引用计数机制为主，标记-清除和分代收集 两种机制为辅的策略」**

[Python垃圾回收机制--完美讲解! - 简书](https://www.jianshu.com/p/1e375fb40506)

##### ① 引用计数机制

- PyObject是每个对象必有的内容，其中`ob_refcnt`就是做为引用计数
- 多一个引用`ob_refcnt` +1，删除一个-1，为0时，对象生命结束
- **优点：**
  - 简单
  - 实时性：一旦没有引用，内存就直接释放了
- **缺点：**
  - 维护引用计数消耗资源
  - 循环引用会造成内存泄漏：比如，有两个类`A、B`，分别创建一个对象`a、b`，让两个对象的属性保留另一个类对象：`a.ref = b`、`b.ref=a `，删除两个对象`del a, del b`。此时两个类互有对方的引用，但却没有一个实际的引用能找到它们。（列表、字典、类、元组都会有这个问题）

##### ② 标记-清除

- 原理
  - 两个链表，一个是**root**链表(root object)，另外一个是**unreachable**链表
  - 它分为两个阶段：第一阶段是标记阶段，GC会把所有的『活动对象』打上标记，第二阶段是把那些没有标记的对象『非活动对象』进行回收
    - 找到其中一端a,开始拆这个a,b的引用环（我们从A出发，因为它有一个对B的引用，则将B的引用计数减1；然后顺着引用达到B，因为B有一个对A的引用，同样将A的引用减1，这样，就完成了循环引用对象间环摘除。），去掉以后发现，a,b循环引用变为了0，所以a,b就被处理到unreachable链表中直接被做掉。
  - 为什么要搞这两个链表：两个对象互相引用，删除a引用。拆环的时候a引用数变为0，进入到unreachable链表中，但b还在，于是又把a拉回到root链表中
- 标记清除算法作为Python的辅助垃圾收集技术主要处理的是一些容器对象，比如list、dict、tuple，instance等
- 缺点：清除非活动的对象前它必须顺序扫描整个堆内存，哪怕只剩下小部分活动对象也要扫描所有对象

##### ③ 分代回收

- 原理
  - 分代回收思想将对象分为三代（generation 0,1,2），0代表幼年对象，1代表青年对象，2代表老年对象。**根据弱代假说（越年轻的对象越容易死掉，老的对象通常会存活更久。）** 新生的对象被放入0代，如果该对象在第0代的一次gc垃圾回收中活了下来，那么它就被放到第1代里面（它就升级了）。如果第1代里面的对象在第1代的一次gc垃圾回收中活了下来，它就被放到第2代里面
  - gc执行的时间，每层不一样（默认 700,10,10）
    - 第一层700是指：创建的对象数 - 删除的对象数 > 700时，执行第一层的清理工作
    - 第二层10：第一层执行完10次，第二层执行1次
    - 第三层10：第二层执行完10次，第三层执行1次
- 分代回收是建立在标记清除技术基础之上。分代回收同样作为Python的辅助垃圾收集技术处理那些容器对象

### 5. 小知识点

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

#### 2 ★socket（套接字） UDP

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

##### （8）udp广播

```python
import socket, sys

# ip地址换成 特殊形式
dest = ('<broadcast>', 7788)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# !!! 对这个需要发送广播数据的套接字修改设置，否则不能发送广播数据
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# 以广播的形式发送数据到本网络的所有电脑中
s.sendto("Hi", dest)
print("等待对方回复（按ctrl+c退出）")
while True:
    (buf, address) = s.recvfrom(2048)
    print("Received from %s: %s" % (address, buf))
```



### （二）TFTP文件下载器、TCP编程

#### 1 wireshark入门使用

##### （1）安装

官网下载安装即可。其中WinPcap（现在改成Ucap）USBPcap都要安装

##### （2）简单使用

- 抓包界面

![2-3-2-1-2_wireshark抓包界面](https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-2-1-2_wireshark%E6%8A%93%E5%8C%85%E7%95%8C%E9%9D%A2.jpg)

- 过滤规则
  - 筛选ip：`ip.src==192.168.25.3`or`ip.dst==192.168.25.4`
  - 网络协议：`udp`、`tcp`等
  - 端口：`udp.port==7777`
  - 多个规则：`规则1 and 规则2` 、`or`

#### 2 TFTP下载器

##### （1）TFTP简介

- Trivial File Transfer Protocol，简单文件传输协议
- TFTP软件界面
  - ![2-3-2-2-1_tftp界面](https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-2-2-1_tftp%E7%95%8C%E9%9D%A2.jpg)

##### （2）TFTP协议

![](https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-2-2-2_tftp%E5%8D%8F%E8%AE%AE.jpg)

##### （3）tftp下载器

[详见代码](.\测试代码\第2章 python核心编程\第3节 网络编程\2 TFTP文件下载器\2_tftp下载器.py)

代码流程：

1. 创建socket
2. 发送下载文件的请求
3. 接收服务发送回来的应答数据
4. 返回响应（正确收到数据）
   or 输出错误代码
5. 写个循环重复接收
6. 当recv_data数据长度小于516跳出循环
7. 向文件中写入
   若请求错误删除文件
8. 错误重传的检查
9. 大文件的块标号循环（最大65535）

#### 3 TCP编程

##### （1）tcp相关介绍

- TCP：Transmission Control Protocol 传输控制协议
  - 特点：稳定、相对UDP慢一点点、web服务器用tcp 
- UDP：User Datagram Protocol 用户数据报协议
  - 特点：不稳定

##### （2）tcp服务器

- `socket(xxx)` —— 买个手机
- `bind(xxx)` —— 插入手机卡（一个固定的电话号码「端口」）
- `listen(xxx)` —— 手机设置为响铃模式？（将套接字变为可以被动链接）
- `accept(xxx)` —— 等待接收电话，接收后会创建一个新的电话（socket）用于和客户端链接
- `recv/send(xxx)` —— 收发数据
- `socket.close()` —— 关闭套接字

```python
from socket import *

# SOCK_STREAM表示tcp通信
serverSocket = socket(AF_INET, SOCK_STREAM)

# 绑定端口
serverSocket.bind(("", 7788))

# 将主动套接字变为被动套接字
serverSocket.listen(5)

# 等待连接，会有一个新的server用于传输数据
clientServer, clientInfo = serverSocket.accept()

# 等待收数据
recv_data = clientServer.recv(1024)
print("%s: %s" % clientInfo, recv_data.decode("gb2312"))

serverSocket.close()
clientSocket.close()
```

##### （3）tcp客户端

- `connect(xxx)`，连接服务器
- `send(xxx)`，发送数据
- `recv(xxx)`，接收数据
- 不再需要向udp那样`sendto() / recvfrom()`中填写对方ip和port，因为一开始已经连接好

```python
from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(("192.168.25.3", 7788))

clientSocket.send(b'haha')
recv_data = clientSocket.recv(1024)
print(recv_data)

clientSocket.close()
```

##### （4）tcp断开连接

- 收到的数据长度 > 0 为链接状态
- 断开链接时数据长度 = 0



### （三）网络通信过程

#### 1 packet tracer介绍

##### （1）小知识点

- 两台电脑通信前提？
  - 在同一网段内
- 多台电脑间为啥不能直接把网线剪开链接在一起？
  - 靠电信号传输数据，接一起电信号就乱了
- 链接多台电脑的hub（集线器，现在已经被交换机代替）的作用？
  - 将多台电脑链接在一起，组一个小型局域网
- 集线器和交换机的区别？
  - 集线器收到的数据都以广播的形式发送出去
  - 交换机有一个学习的过程，第一次是广播，但学习到路径之后，后面的就不用再广播传了

##### （2）交换机组网

同一个局域网内互相`ping`

- 得有对方的MAC地址才能ping通
  - 第一次：PC发送一个ARP的广播，由交换机广播出去；对应IP的PC接收到广播后，返回一个ARP；交换机记下该IP的MAC地址；再把这个ARP返回给原PC；然后才发送ping的ICMP包
  - <img src="https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-3-1-2_%E4%BA%A4%E6%8D%A2%E6%9C%BAping%E6%B5%81%E7%A8%8B.gif" width=50%>
  - 第二次：交换机已经记住了另一台电脑的MAC地址，直接发送ICMP包就行了
  - <img src="https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-3-1-2_%E4%BA%A4%E6%8D%A2%E6%9C%BA%E6%B5%81%E7%A8%8B%E8%A7%A3%E9%87%8A.jpg"/>

##### （3）路由器组网

路由器的作用

- 链接不同网段的电脑，使其可以通信
  - 使用交换机只能在同一个网段内通信，即便把两个网段的交换机用网线连起来也不能用
- 配置
  - <img src="https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-3-1-3_%E8%B7%AF%E7%94%B1%E5%99%A8%E7%BB%84%E7%BD%91.jpg" width=70% />
  - 左边一个网段，右边一个网段；路由器的两侧的网卡链接不同的网段；每个主机网关要配置成路由器的IP
- 多路由器组网配置
  - <img src="https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-3-1-3_%E5%A4%9A%E8%B7%AF%E7%94%B1%E5%99%A8%E7%BB%84%E7%BD%911.jpg" width=70%/>
  - 这里还需要给每一个路由器写好路由表
    - 比如192.168.1.x的PC给192.168.2.x的PC通信，传到第一个路由器的时候，路由器不知道该把包往哪里发，就需要手动配置一下（下图是第一个路由器的配置）
    - 将包转给第二个路由器；来回的路线都需要配置
    - <img src="https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-3-1-3_%E8%B7%AF%E7%94%B1%E5%99%A8%E7%9A%84%E9%9D%99%E6%80%81%E8%B7%AF%E7%94%B1%E9%85%8D%E7%BD%AE.jpg"/>

#### 2 通信过程

##### （1）★ mac地址和ip地址用途

- mac地址：在两个设备之间通信时会变化，指向的是下一个终端
- ip地址：整个通信过程中都不会变化，一直指向的最终的位置
- ip：标记逻辑上的地址
- mac：标记实际转发数据时的设备地址
- netmask：和ip地址一起确定网络号
- 默认网关：发送的ip不再同一个网段内，就会把这个数据转发给网关

##### （2）DNS

- dns协议是用来解析域名的一个协议
  - 一个dns服务器上存了很多域名对应的ip地址
  - 相当于一个电话簿，姓名-域名， 电话-ip地址
- 在终端PC上要配置DNS服务器地址

##### （3）访问百度的过程

1. 解析`www.baidu.com`对应的ip地址
   1. 先知道默认网关mac
      1. 使用arp获取默认网关的mac地址
   2. 组织数据，发送给默认网关（ip一直为dns服务器的ip的，但mac地址是默认网关的mac地址）
   3. 默认网关拥有转发数据的能力，把数据转发给路由器
   4. 路由器根据自己的路由协议，选择一个合适的较快的路径转发数据给目的网关
   5. 目的网关（dns服务器所在的网关），把数据转发给dns服务器
   6. dns服务器解析出对应的ip地址，并把数据原路返回给请求的client
2. 得到ip之后，发送tcp三次握手，进行连接
3. 使用http协议发送请求数据给web服务器
4. web服务器收到数据请求后进行查询，将查询结果原路返回给client的浏览器
5. 浏览器接收到数据后，通过渲染功能显示网页
6. 浏览器关闭tcp连接，即4次挥手

##### （4）TCP三次握手、四次挥手

- 三次握手
  - 第二次有两个码，一个是对client发来的码+1，另一个是发送自己的一个新码，用于确认client是否在线
- 四次挥手
  - 双方互相告知通信结束，并发送ACK确认码
- TCP为保证数据的安全性，每次发送数据后，对方都会发送一个ACK应答码（表示接收到数据）

<img src="https://raw.githubusercontent.com/shuopic/ImgBed/master/%E4%BC%A0%E6%99%BApython%E5%B0%B1%E4%B8%9A%E7%8F%AD/2-3-3-2-4_tcp%E4%B8%89%E6%AC%A1%E6%8F%A1%E6%89%8B%E5%9B%9B%E6%AC%A1%E6%8C%A5%E6%89%8B.jpg"/>