"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F
"""

from fei.ppds import Thread
from fei.ppds import Event
from fei.ppds import Mutex
from fei.ppds import RandomSemaphore, Semaphore

class SynchronizationHelper:
    """
    Helper class for synchronization while calculation fibonacci sequence.
    Represents a barrier
    """
    def __init__(self, n):
        """
        Initialization method

        Attributes:
            numberOfThreads  Number of threads
            counter          Count of how many threads are waiting at the barrier
            indexCounter     Counter for index in fibonacci sequence
            everyIsCreated   A synchronization object (Semaphore or Event)
            mutex            Mutex for barrier

        :param n: number of threads
        """
        self.numberOfThreads = n
        self.counter = 0
        self.indexCounter = 0
        self.everyIsCreated = Semaphore(0)
        self.mutex = Mutex()

    def wait_for_creation(self):
        """
        Main method of barrier. Threads are gathered here and then after that,
        they start computing sequence. We can use in init method Event() or
        Semaphore(0) initialization of attribute everyIsCreated.
        :return: none
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.numberOfThreads and \
                isinstance(self.everyIsCreated, RandomSemaphore):
            self.everyIsCreated.signal(self.numberOfThreads)
        elif self.counter == self.numberOfThreads:
            self.everyIsCreated.signal()
        self.mutex.unlock()
        self.everyIsCreated.wait()

def compute_fibonacci(sh, mutex):
    """
    This function computes fibonacci sequence. It uses shared index into sequence and
    is called by multiple threads.
    :param sh: Synchronization helper
    :param mutex: Global mutex
    :return: none
    """
    print("before wait")
    sh.wait_for_creation()
    mutex.lock()
    fib_seq[sh.indexCounter+2] = fib_seq[sh.indexCounter] + fib_seq[sh.indexCounter+1]
    sh.indexCounter += 1
    mutex.unlock()

if __name__ == "__main__":
    """
    Entry point of program
    """
    THREADS = 10
    COEFFICIENT = 1
    helper = SynchronizationHelper(THREADS)
    m = Mutex()

    fib_seq = [0] * (THREADS + 2)
    fib_seq[1] = 1

    threads = [Thread(compute_fibonacci, helper, m) for i in range(THREADS)]
    [t.join() for t in threads]

    print(fib_seq)