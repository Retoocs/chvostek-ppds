from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread, print

class Shared(object):
    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)

def producer(shared):
    while True:
        sleep(randint(1, 10)/10)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.free.signal(1)
        shared.items.signal()


def consumer(shared):
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        sleep(randint(1, 10) / 10)

if __name__ == "__main__":
    for i in range(10):
        s = Shared(10)
        c = [Thread(consumer, s) for _ in range(2)]
        p = [Thread(producer, s) for _ in range(5)]
        sleep(5)
        s.finished = True
        print(f"hl vlakno {i}: caka na dokoncenie")
        s.items.signal(100)
        s.free.signal(100)
        [t.join() for t in c+p]
        print(f"hl vlakno {i}: koniec programu")
