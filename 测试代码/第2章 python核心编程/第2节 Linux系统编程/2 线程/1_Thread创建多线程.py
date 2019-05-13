from threading import Thread
from time import sleep

def fun():
    print("hahaha")
    sleep(1)

for i in range(5):
    t = Thread(target=fun)
    t.start()