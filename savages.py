
from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self, fullPot=None, last_thread_signal=False):
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
    def __init__(self, C):
        self.mutexSavage = Mutex()
        self.mutexCook = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(C)
        self.barrier2 = SimpleBarrier(C)


def get_serving_from_pot(savage_id, shared):
    print("savage %2d: taking a portion" % savage_id)
    shared.servings -= 1

def eat(savage_id):
    print("savage %2d: eating" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)

def savage(savage_id, shared, C):
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
    print(f"cook    {cook_id}: inserting portions")
    shared.servings += M


def cook(M, shared, cook_id):
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
    main()