"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/
"""

from collection.Collection import Counter
from fei.ppds import Thread

class Shared():
    """
    Saves a list of number elements. Contains counter and size attribute
    """
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size

def do_count(shared):
    """
    Gets an object shared, that has a list of numbers and increments every element by one

    :param shared: an instance of class Shared
    :return: none
    """
    while True:
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1

shared = Shared(1000000)
t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)
t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())
