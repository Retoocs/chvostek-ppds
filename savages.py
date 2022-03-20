"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/
"""
from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    """
    Synchronization object of type Barrier
    """
    def __init__(self, N):
        """
        Initialization method
        :param N: Number of threads to stop
        """
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self, fullPot=None, last_thread_signal=False):
        """
        Method to block threads.
        :param fullPot: Synchronization object of type Semaphore
        :param last_thread_signal: If true, fullPot.signal() is called with the last thread
        :return: None
        """
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            if last_thread_signal:
                fullPot.signal()
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    """
    Shared object to store needed variables
    """
    def __init__(self, C):
        """
        Initialization method
        :param C: Number of cooks

        Attributes:
            - mutexSavage: mutex for savage thread
            - mutexCook: mutex for cook thread
            - servings: actual number of servings in pot
            - full_pot: Semaphore to signal pot is full
            - empty_pot: Semaphore to signal pot is empty
            - barrier1, barrier2: barriers for cook threads
        """
        self.mutexSavage = Mutex()
        self.mutexCook = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(C)
        self.barrier2 = SimpleBarrier(C)


def get_serving_from_pot(savage_id, shared):
    """
    Function simulates taking portions
    :param savage_id: savage identifier
    :param shared: shared helper object
    :return: None
    """
    print("savage %2d: taking a portion" % savage_id)
    shared.servings -= 1

def eat(savage_id):
    """
    Function simulates savage eating
    :param savage_id: savage identifier
    :return:
    """
    print("savage %2d: eating" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)

def savage(savage_id, shared, C):
    """
    Function for savage thread
    :param savage_id: Savage identifier
    :param shared: shared helper object
    :param C: number of cooks
    :return: None
    """
    while True:
        shared.mutexSavage.lock()
        print("savage %2d: portions left in pot: %2d" % (savage_id, shared.servings))
        if shared.servings == 0:
            print("savage %2d: waking up cooks" % savage_id)
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutexSavage.unlock()

        eat(savage_id)


def put_servings_in_pot(M, shared, cook_id):
    """
    Function simulates putting portions
    :param M: capacity of pot
    :param shared: shared helper object
    :param cook_id: cook identifier
    :return: None
    """
    print(f"cook    {cook_id}: inserting portions")
    shared.servings += M


def cook(M, shared, cook_id):
    """
    Function for cook thread
    :param M: capacity of pot
    :param shared: shared helper object
    :param cook_id: cook identifier
    :return: None
    """
    while True:
        shared.empty_pot.wait()
        print(f"cook    {cook_id}: cooking")
        sleep(randint(1, 3) / 100)

        shared.mutexCook.lock()
        if shared.servings == 0:
            put_servings_in_pot(M, shared, cook_id)
        shared.mutexCook.unlock()
        shared.barrier1.wait()
        shared.barrier2.wait(
            fullPot=shared.full_pot,
            last_thread_signal=True
        )


def main():
    """
    Main function of the program. Configures program and creates threads
    :return: None
    """
    # savages
    N = 3
    # pot capacity
    M = 2
    # cooks
    C = 5
    threads = list()
    shared = Shared(C)

    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared, C))
    for cook_id in range(0, C):
        threads.append(Thread(cook, M, shared, cook_id))

    for t in threads:
        t.join()


if __name__ == "__main__":
    """
    Entry point of program
    """
    main()