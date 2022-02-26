from random import randint
from time import sleep
from fei.ppds import Thread
from fei.ppds import Mutex
from fei.ppds import Event
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, n):
        self.numberOfThreads = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.numberOfThreads:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("Thread %d is BEFORE barrier" % thread_id)
    barrier.wait()
    print("Thread %d is AFTER barrier" % thread_id)


if __name__ == "__main__":
    THREADS = 10
    sb = SimpleBarrier(THREADS)
    threads = [Thread(barrier_example, sb, i) for i in range(THREADS)]
    [t.join() for t in threads]