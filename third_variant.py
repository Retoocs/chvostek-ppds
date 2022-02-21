"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/
"""
import time

from collection.Collection import Counter
from fei.ppds import Thread
from fei.ppds import Mutex

class Shared():
    """
    Saves a list of number elements. Contains counter and size attribute
    """
    def __init__(self, size):
        """
        Initializes an instance of Shared
        :param size: length of the attribute elms
        """
        self.counter = 0
        self.end = size
        self.elms = [0] * size

def do_count(shared, mutex):
    """
    Gets an object shared, that has a list of numbers and increments every element by one

    :param shared: an instance of class Shared
    :param mutex: a global lock, which threads use
    :return: none
    """
    mutex.lock()

    while True:
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1

    mutex.unlock()

if __name__ == "__main__":
    """
    The entry point of program. Creates a global lock and instance of class Shared
    """
    start = time.time()

    mutex = Mutex()
    shared = Shared(1_000_000)
    t1 = Thread(do_count, shared, mutex)
    t2 = Thread(do_count, shared, mutex)
    t1.join()
    t2.join()

    counter = Counter(shared.elms)
    print(counter.most_common())

    end = time.time()
    print('Elapsed time: ' + str(round(end - start, 8)) + " sec")
