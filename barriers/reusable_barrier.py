"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F
"""

from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Event
from fei.ppds import print


class SimpleBarrier:
    """
    Reusable synchronization object of type barrier
    """
    def __init__(self, n):
        """
        Initialization method
        :param n: number of threads
        """
        self.numberOfThreads = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
        Main method of barrier. Threads wait here to continue
        :return: none
        """
        self.event.clear()
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.numberOfThreads:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()

def before_rendezvous(thread_name):
    """
    Helper function. Prints text before rendezvous section
    :param thread_name: name of current thread
    :return: none
    """
    print('%s: BEFORE rendezvous' % thread_name)

def rendezvous(thread_name):
    """
    Helper function. Simulates rendezvous section
    :param thread_name: name of current thread
    :return: none
    """
    #sleep(randint(1, 10) / 10)
    print('%s: rendezvous' % thread_name)

def critical_area(thread_name):
    """
    Helper function. Simulates critical area
    :param thread_name: name of current thread
    :return: none
    """
    print('%s: critical area' % thread_name)
    #sleep(randint(1, 10) / 10)

def barrier_example(sb1, sb2, sb3, thread_name):
    """
    This function simulates usage of reusable barries. It uses total of 3 barrier's objects
    :param sb1: First barrier
    :param sb2: Second barrier
    :param sb3: Third barrier
    :param thread_name: name of the current thread
    :return: none
    """
    ITERATIONS = 5
    for i in range(ITERATIONS):
        before_rendezvous(thread_name)
        sb1.wait()
        rendezvous(thread_name)
        sb2.wait()
        critical_area(thread_name)
        sb3.wait()

if __name__ == "__main__":
    """
    The entry point of program. It creates 3 barriers and multiple threads
    """
    THREADS = 4
    simpleBarrier1 = SimpleBarrier(THREADS)
    simpleBarrier2 = SimpleBarrier(THREADS)
    simpleBarrier3 = SimpleBarrier(THREADS)
    threads = [Thread(barrier_example, simpleBarrier1, simpleBarrier2, simpleBarrier3,
                      'Thread %d' % i) for i in range(THREADS)]
    [t.join() for t in threads]