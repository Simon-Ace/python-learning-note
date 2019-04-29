# 第2章 python核心编程

## （一）python核心编程

### 1. 

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



---

### 小知识点：

1. 获取模块查找路径

   ```python
   import sys
   sys.path
   
   # 添加路径
   sys.path.append("path-to-your-file")
   ```

   