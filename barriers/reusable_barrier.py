from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Event
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
        self.event.clear()

def before_rendezvous(thread_name):
    print('%s: BEFORE rendezvous' % thread_name)

def rendezvous(thread_name):
    #sleep(randint(1, 10) / 10)
    print('%s: rendezvous' % thread_name)

def critical_area(thread_name):
    print('%s: critical area' % thread_name)
    #sleep(randint(1, 10) / 10)

def barrier_example(sb, thread_name):
    ITERATIONS = 10
    for i in range(ITERATIONS):
        before_rendezvous(thread_name)
        sb.wait()
        rendezvous(thread_name)
        sb.wait()
        critical_area(thread_name)
        sb.wait()

if __name__ == "__main__":
    THREADS = 5
    simpleBarrier = SimpleBarrier(THREADS)
    threads = [Thread(barrier_example, simpleBarrier, 'Thread %d' % i) for i in range(THREADS)]
    [t.join() for t in threads]