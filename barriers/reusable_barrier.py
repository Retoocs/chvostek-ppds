from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore

"""Vypisovat na monitor budeme pri zamknutom mutexe pomocou
funkcie 'print' z modulu 'fei.ppds', aby sme nemali rozbite vypisy.
"""
from fei.ppds import print


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name):
    """Kazde vlakno vykonava kod funkcie 'barrier_example'.
    Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    nielen pred vykonanim funkcie 'ko', ale aj
    *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
    """

    while True:
        # ...
        rendezvous(thread_name)
        # ...
        ko(thread_name)
        # ...


"""Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
threads = list()
for i in range(5):
    t = Thread(barrier_example, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()