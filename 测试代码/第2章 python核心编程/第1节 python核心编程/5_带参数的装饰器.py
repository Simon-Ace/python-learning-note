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