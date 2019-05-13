def decor(func):
    def decor_in(*args, **kwargs):
        print("----log日志----")
        ret = func(*args, **kwargs)
        return ret
    return decor_in


def ori_func(a, b):
    pass