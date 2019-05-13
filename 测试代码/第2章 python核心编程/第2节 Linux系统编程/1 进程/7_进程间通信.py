'''
进程间通信，如实现进程间数据传递的功能
可使用Queue()进行数据传递
'''

# from time import sleep
# from multiprocessing import Queue, Process, Pool
#
# def read_from_queue(que:Queue):
#     while not que.empty():
#         print("---read: %s----" % que.get())
#         sleep(1)
#
# def write_to_queue(que:Queue):
#     for value in ['A', 'B', 'C']:
#         print("----write: %s----" % value)
#         que.put(value)
#         sleep(1)
#
# que = Queue()
# pw = Process(target=write_to_queue, args=(que,))
# pr = Process(target=read_from_queue, args=(que,))
#
# if __name__ == '__main__':
#     pw.start()
#     pw.join()
#
#     pr.start()
#     pr.join()


# ----------------------------------
'''
进程池Pool间通信
'''
from multiprocessing import Manager,Pool
import os, time


def reader(q):
    print("reader启动(%s),父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in range(q.qsize()):
        print("reader从Queue获取到消息：%s"%q.get(True))
        time.sleep(1)


def writer(q):
    print("writer启动(%s),父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in "dongGe":
        q.put(i)
        print("写入数据到队列：%s" % i)
        time.sleep(1)


if __name__ == "__main__":
    print("(%s) start" % os.getpid())
    q = Manager().Queue()  # 使用Manager中的Queue来初始化
    po = Pool()
    # 使用阻塞模式创建进程，这样就不需要在reader中使用死循环了，可以让writer完全执行完成后，再用reader去读取
    po.apply(writer,(q,))
    po.apply(reader,(q,))
    po.close()
    po.join()
    print("(%s) End"%os.getpid())