# 第2章 python核心编程

## （一）python核心编程

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



## （二）Linux系统编程

### 1 多任务

（1） 进程

并发：看上去一起执行（任务数量 > 核数）  
并行：真正一起执行

（2）线程