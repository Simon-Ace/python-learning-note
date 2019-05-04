# # 斐波那契数列
# def creatNum():
#     a, b = 0, 1
#     for i in range(10):
#         yield b
#         a, b = b, a+b
#
# a = creatNum()
# for i in a:
#     print(i)


# send 用法
def test_fun():
    i = 0
    while i < 5:
        temp = yield i
        print(temp)
        i += 1

a = test_fun()
print(next(a))
a.send("haha")