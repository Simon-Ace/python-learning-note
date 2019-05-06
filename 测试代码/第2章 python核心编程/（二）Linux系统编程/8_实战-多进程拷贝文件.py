'''
实战——多线程拷贝文件
主要体现多线程用法，简化了文件目录，只考虑单层文件目录情况
'''

import os
from time import sleep
from tqdm import tqdm
from multiprocessing import Pool, Manager


def copy_file_task(old_file_path: str, new_file_path: str, queue):
    with open(old_file_path, 'rb') as fr:
        with open(new_file_path, 'wb') as fw:
            # print(os.getpid())
            sleep(1)
            content = fr.read()
            fw.write(content)
            queue.put(new_file_path)


def main():
    # 获取要复制的文件夹名
    old_dir_path = input("please input the folder path to copy: ")
    print("---old path: " + old_dir_path)
    if not os.path.exists(old_dir_path):
        print("the directory does not exist!")
        exit()

    # 创建新的文件夹
    new_dir_path = old_dir_path + 'copy'
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    print("---new path: " + new_dir_path)

    # 获取所有文件名
    filenames = os.listdir(old_dir_path)

    queue = Manager().Queue()

    # 复制
    po = Pool(5)
    for each_file in filenames:
        old_file_path = old_dir_path + '/' + each_file
        new_file_path = new_dir_path + '/' + each_file
        po.apply_async(copy_file_task, args=(old_file_path, new_file_path, queue))

    # po.close()
    # po.join()

    # 主线程用于统计执行进度
    num = 0
    allNum = len(filenames)

    while num < allNum:
        queue.get()
        num += 1
        copy_rate = num / allNum
        print("\rprocessing: %.2f%%" % (copy_rate*100), end="")


if __name__ == '__main__':
    main()
