from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex

"""Vypisovat na monitor budeme pomocou funkcie 'print'
   importovanej z modulu 'ppds'.
   To kvoli tomu, aby neboli 'rozbite' vypisy.
"""
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        # ...

    def wait(self):
        # ...
        pass


def barrier_example(barrier, thread_id):
    """Predpokladajme, ze nas program vytvara a spusta 5 vlakien,
    ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
    zdielany objekt jednoduchej bariery
    """
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


# priklad pouzitia ADT SimpleBarrier
sb = SimpleBarrier(5)

# doplnit kod, v ktorom sa vytvara a spusta 5 vlakien
# ...