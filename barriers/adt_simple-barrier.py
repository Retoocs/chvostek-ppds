"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F
"""

from random import randint
from time import sleep
from fei.ppds import Thread
from fei.ppds import Mutex
from fei.ppds import Event
from fei.ppds import print


class SimpleBarrier:
    """
    A synchronization object of kind barrier
    """
    def __init__(self, n):
        """
        Initialization method
        :param n: represents number of threads
        """
        self.numberOfThreads = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
        Main method of barrier object. Threads wait in this function to continue
        :return: none
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.numberOfThreads:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()


def barrier_example(barrier, thread_id):
    """
    An example function, that simulates barrier usage. It prints text before and after barrier
    :param barrier: synchronization object
    :param thread_id: id of current thread
    :return:
    """
    sleep(randint(1, 10) / 10)
    print("Thread %d is BEFORE barrier" % thread_id)
    barrier.wait()
    print("Thread %d is AFTER barrier" % thread_id)


if __name__ == "__main__":
    """
    The entry point of program. Threads are here created
    """
    THREADS = 10
    sb = SimpleBarrier(THREADS)
    threads = [Thread(barrier_example, sb, i) for i in range(THREADS)]
    [t.join() for t in threads]