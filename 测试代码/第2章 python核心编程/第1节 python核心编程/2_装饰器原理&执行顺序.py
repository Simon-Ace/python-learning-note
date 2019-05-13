# def w1(func):
#     def inner():
#         print("----正在验证权限----")
#         if True:
#             return func()
#         else:
#             print("----没有权限----")
#     return inner
#
# @w1
# def f1():
#     print("----f1----")
#
# f1()
#
# # 执行原理
# f1 = w1(f1)
# f1()





# ---------------------------------------------------
#
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