"""
todo
"""
from queue import Queue
from random import randint
from fei.ppds import Mutex, Semaphore, print, Thread
from time import sleep

class SynchHelper:
    def __init__(self, capacity):
        self.mutex = Mutex()
        self.queue = Queue()
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)
        self.customers = 0
        self.shopCapacity = capacity

def getHairCut(customerId):
    print(f"Customer {customerId}: getting haircut...")

def balk(customerId):
    print(f"Customer {customerId}: I'll come next time")

def customer(customerId, helper):
    while True:
        sleep(randint(4, 6) / 10)
        helper.mutex.lock()
        if helper.customers == helper.shopCapacity:
            helper.mutex.unlock()
            balk(customerId)
        else:
            helper.customers += 1
            myTicket = Semaphore(0)
            print(f"Customer {customerId}: waiting for haircut")
            helper.mutex.unlock()
            helper.queue.put(myTicket)
            helper.customer.signal()
            myTicket.wait()

            getHairCut(customerId)

            helper.customerDone.signal()
            helper.barberDone.wait()

            helper.mutex.lock()
            print(f"Customer {customerId}: thanks")
            helper.customers -= 1
            helper.mutex.unlock()

def cutHair(barberId):
    print(f"Barber   {barberId}: cutting...")

def barber(barberId, helper):
    while True:
        print(f"Barber   {barberId}: waiting for customer")
        helper.customer.wait()
        aTicket = helper.queue.get()
        aTicket.signal()

        cutHair(barberId)

        helper.customerDone.wait()
        helper.barberDone.signal()

def main():
    N = 20
    C = 3
    threads = list()
    helper = SynchHelper(C)

    threads.append(Thread(barber, 0, helper))
    for customerId in range(N):
        threads.append(Thread(customer, customerId, helper))

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()