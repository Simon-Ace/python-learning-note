from threading import Thread, Lock
from time import sleep

def fun1():
    while True:
        if lock1.acquire():
            print("----task1----")
            sleep(0.5)
            lock2.release()

def fun2():
    while True:
        if lock2.acquire():
            print("----task2----")
            sleep(0.5)
            lock3.release()

def fun3():
    while True:
        if lock3.acquire():
            print("----task3----")
            sleep(0.5)
            lock1.release()

lock1 = Lock()
lock2 = Lock()
lock3 = Lock()

lock2.acquire()
lock3.acquire()

t1 = Thread(target=fun1)
t2 = Thread(target=fun2)
t3 = Thread(target=fun3)

t1.start()
t2.start()
t3.start()

