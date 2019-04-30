class Test(object):
    def __init__(self):
        self.__num = 100

    @property
    def num1(self):
        print("----getter----")
        return self.__num

    @num1.setter
    def num1(self, newNum):
        print("----setter----")
        self.__num = newNum


t = Test()
t.num1 = 100
print(t.num1)