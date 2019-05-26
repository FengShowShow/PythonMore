import multiprocessing
import numpy as np
import time

class MyArrayClass:
    def __init__(self, array):
        self.array = array

    def add_one(self):
        self.array = self.array + 1
        return self.array

def worker(in_q, out_q):
    name = multiprocessing.current_process().name
    print(name)
    obj = in_q.get()
    array = obj.add_one()
    out_q.put(array)
    print('exit pid: ', name)
    time.sleep(2)

def check_len(in_q):
    while 1:
        print('in size:', in_q.qsize())
        time.sleep(1)

def main():

    pool_size = multiprocessing.cpu_count()
    print('max process:', multiprocessing.cpu_count())
    in_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()
    dae = multiprocessing.Process(target=check_len, args=(in_queue,))
    dae.daemon = True

    # a queue of nd array to be process
    a = MyArrayClass(np.zeros((2, 2)))
    b = MyArrayClass(np.zeros((4, 4)))
    in_queue.put(a)
    in_queue.put(b)

    p = multiprocessing.Process(target=worker, args=(in_queue, out_queue,))
    # p = multiprocessing.Pool()
    # for n in range(1):
    #     # non block
    #     p.apply_async(worker, args=(in_queue, out_queue,))
    dae.start()
    # time.sleep(1)

    # dae.join()
    #p.close()
    p.start()
    p.join()
    print(in_queue.qsize(), out_queue.qsize())
    # print(queue.get())

if __name__ == '__main__':
   main()
