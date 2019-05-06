# 第2章 python核心编程

[TOC]

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

### （一）多任务

#### 1 进程

并发：看上去一起执行（任务数量 > 核数）  
并行：真正一起执行

##### （1）fork创建子进程

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

##### （2）全局变量在多个进程中不共享

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

##### （3）fork炸弹

```python
#永远不要写下面这种代码！
while True:
    os.fork()
```

##### （4）使用Process创建进程

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

##### （5）join()进程阻塞

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

##### （6）Process子类

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

##### （7）进程池Pool

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

##### （8）进程间通信

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

##### （9）实战：多进程拷贝文件

- 详见代码

#### 2 线程