from fei.ppds import Thread
from fei.ppds import Event
from fei.ppds import Mutex
from fei.ppds import RandomSemaphore, Semaphore

class SynchronizationHelper:
    def __init__(self, n):
        self.numberOfThreads = n
        self.counter = 0
        self.indexCounter = 0
        self.everyIsCreated = Semaphore(0)
        self.mutex = Mutex()

    def wait_for_creation(self):
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
    print("before wait")
    sh.wait_for_creation()
    mutex.lock()
    fib_seq[sh.indexCounter+2] = fib_seq[sh.indexCounter] + fib_seq[sh.indexCounter+1]
    sh.indexCounter += 1
    mutex.unlock()

if __name__ == "__main__":
    THREADS = 10
    COEFFICIENT = 1
    helper = SynchronizationHelper(THREADS)
    m = Mutex()

    fib_seq = [0] * (THREADS + 2)
    fib_seq[1] = 1

    counter = 0
    threads = [Thread(compute_fibonacci, helper, m) for i in range(THREADS)]
    [t.join() for t in threads]

    print(fib_seq)