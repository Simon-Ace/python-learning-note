def test_fun(number):
    def test_in(number2):
        print(number + number2)
    return test_in

ret = test_fun(100)
ret(1)
ret(200)


# -----------------------------------
# 改变外部变量的值

def test_fun(number):
    def test_in(number2):
        nonlocal number
        number = number + number2
        print(number)

    return test_in

ret = test_fun(100)
ret(1)
ret(200)