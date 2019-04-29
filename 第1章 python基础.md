# 第1章 python基础

## （一）面向对象

**1. 私有方法：**

函数**前面**加两个下划线，“__”

**2. 类中魔法方法：**

- _\_new\_\_(self)

  创建类实例时调用的方法

  ```python
  def __new__(cls):
      print("--------new方法---------")
      return object.__new__(cls) #这句一定要有，调用父类中的方法，完成对象的创建
  ```

- \_\_init\_\_(self)

  初始化类实例时调用的方法

- \_\_str\_\_(self)

  print实例时调用的方法

- \_\_del\_\_(self)

  当对象的所有引用都删除后，会执行该方法，若程序结束时还有引用，会自动执行该方法

`dahuang = Dog()`

这个话做了三件事：

​	(1) 调用_\_new\_\_(self)创建对象，然后找一个变量接收_\_new\_\_(self)的返回值，返回值为创建出来的对象的引用  
​	(2) 调用_\_init\_\_(self)  
​	(3) 返回对象的引用

**3. 引用个数：**

`sys.geterefcount(引用名)`

计算对象的引用个数，比实际多一个，因为执行该方法时会多生成一个引用

**4. 继承：**

`class 子类(父类)`

**5. 重写：**

**6. 调用被重写的方法：**

两种写法

```python
class 子类(父类):
    def 重写函数(self):
        # 调用父类方法 ①
        父类.函数(self)
        # 方法②  - 推荐
        super().bark()
```



**7. 多继承：**

当子类继承的两个父类对同一个方法都进行重写时，调用的先后顺序可由`类名.__mro__`查看。

注意！最好不要出现这种情况

若出现了这种情况，但是要调用非python自定顺序的父类函数，可用「类名来指定」：

`父类.多次被重写的函数名(self)`

**8.  多态：**

> 多态是同一个行为具有多个不同表现形式或形态的能力。
>
> 多态就是同一个接口，使用不同的实例而执行不同操作。

一个引用 执行 函数，定义的时候不知道调那个类中函数，执行的时候才确定

> 1.要有继承关系
> 2.子类要重写父类的方法
> 3.父类引用指向子类

同一个函数名，不同参数 叫什么？ —— 重载

**9. 类对象、实例对象：**

定义类的时候会有一个类对象，包含类属性和方法

创建实例的时候会有一个实例对象，里面仅有实例属性，不保存类方法；其中包含一个特殊的属性——能够知道这个对象的class，调用函数的时候去类对象里面找

**10. 类属性、实例属性：**

- 实例属性

  和具体的某个实例对象有关系，实例对象间不共享属性

- 类属性

  所有对象共享

```python
class  Tool(object):
    # 类属性
    num = 0
    
    def __init__(self, new_name):
        # 实例属性
        self.name = new_name
        # 使用类属性
        Tool.num += 1
```

**11. 实例方法、类方法、静态方法：**

类方法加装饰器 `@classmethod`  
静态方法加 `@staticmethod`，静态方法完成一些最基本的功能，既和类没关系也和实例对象没关系

【装饰器：概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能】  
[理解 Python 装饰器看这一篇就够了](https://foofish.net/python-decorator.html)

★ 设计的时候，操作类属性的使用类方法；操作实例属性的使用实例方法；和类属性实例属性都无关，使用静态方法

```python
class Game(object):
    # 类属性
    num = 0
    
    # 实例方法
    def __init__(self):
        pass
    
    # 类方法
    @classmethod
    def add_num(cls):
        cls.num = 100   
        
    # 静态方法
    @staticmethod
    def print_menu():	#不用写self参数
        print("start game....")
```

类方法、静态方法调用：

```python
game = Game()
# 类方法
Game.add_num()	#通过类名调用
game.add_num()	#通过类对象调用

# 静态方法也是两种都可以
Game.print_menu()
game.print_menu()
```

**12. 为什么要继承 object 类？**z

继承 object 类的是新式类，不继承 object 类的是经典类，在 Python 2.7 里面新式类和经典类在多继承方面会有差异，在 Python 3.x 中的新式类貌似已经兼容了经典类

- 经典类按照**深度**优先的方法去搜索（多继承冲突的时候）
- 新式类按照**广度**优先的方法去搜索

**13. 单例模式：**

```python
class Dog(object):
    __instance = None
    def __new__(cls):
        if cls__instance == None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance
        
a = Dog()
print(id(a))
b = Dog()
print(id(b))
```

