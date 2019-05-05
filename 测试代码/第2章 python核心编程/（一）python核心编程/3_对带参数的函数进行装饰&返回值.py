# #简单写法（不推荐）
# def decor(func):
#     def decor_in(a, b):
#         print("----decorate func----")
#         func(a, b)
#     return decor_in
#
# @decor
# def ori_func(a, b):
#     print("----ori_func: %d, %d----" % (a, b))
#
#
# ori_func(1,2)

# ----------------------

# 不定长参数通用写法（推荐）
# def decor(func):
#     def decor_in(*args, **kwargs):
#         print("----decorate func----")
#         func(*args, **kwargs)
#     return decor_in
#
# @decor
# def ori_func(a, b):
#     print("----ori_func: %d, %d----" % (a, b))
#
# @decor
# def ori_func1(a, b, c):
#     print("----ori_func1: %d, %d, %d----" % (a, b, c))
#
#
# ori_func(1,2)
# ori_func1(3, 4, 5)

# -----------------------

# 对带返回值的函数进行装饰
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


# 通用写法
# 带参数的装饰器

