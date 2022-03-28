"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/
"""
from queue import Queue
from random import randint
from fei.ppds import Mutex, Semaphore, print, Thread
from time import sleep

class SynchHelper:
    """
    Helper class for synchronization

    Attributes:
        - mutex: Synchronization object of type Mutex
        - queue: queue of customer's tickets
        - customer: Semaphore. Simulates customer's arrival
        - customerDone: Semaphore. Simulates customer wants to finish
        - barberDone: Semaphore. Simulates barber wants to finish
        - customers: number of customers in shop
        - shopCapacity: maximum shop capacity
    """
    def __init__(self, capacity):
        """
        Initialization method
        :param capacity: maxium capacity of barber shop
        """
        self.mutex = Mutex()
        self.queue = Queue()
        self.customer = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)
        self.customers = 0
        self.shopCapacity = capacity

def customer(customerId, helper):
    """
    Process for customer thread.

    Local variables:
        - myTicket: Semaphore. Barber can call particular customer by this object in queue

    :param customerId: identifier of customer thread
    :param helper: helper synchronization object
    :return: None
    """
    while True:
        # simulation of hair growth
        sleep(randint(4, 6) / 10)
        helper.mutex.lock()
        if helper.customers == helper.shopCapacity:
            helper.mutex.unlock()
            print(f"Customer {customerId}: I'll come next time")
        else:
            helper.customers += 1
            myTicket = Semaphore(0)
            print(f"Customer {customerId}: waiting for haircut")
            helper.mutex.unlock()
            helper.queue.put(myTicket)
            helper.customer.signal()
            myTicket.wait()

            print(f"Customer {customerId}: getting haircut...")

            helper.customerDone.signal()
            helper.barberDone.wait()

            helper.mutex.lock()
            print(f"Customer {customerId}: thanks")
            helper.customers -= 1
            helper.mutex.unlock()

def barber(barberId, helper):
    """
    Process for barber thread.

    Local variables:
        - aTicket: A ticket, that owns the customer

    :param barberId: identifier of barber
    :param helper: helper synchronization object
    :return: None
    """
    while True:
        print(f"Barber   {barberId}: waiting for customer")
        helper.customer.wait()
        aTicket = helper.queue.get()
        aTicket.signal()

        print(f"Barber   {barberId}: cutting...")

        helper.customerDone.wait()
        helper.barberDone.signal()

def main():
    """
    Main function of the program. Configures program and creates threads
    :return: None
    """
    # number of customers
    N = 20
    # maximum shop capacity
    C = 3
    threads = list()
    helper = SynchHelper(C)

    threads.append(Thread(barber, 0, helper))
    for customerId in range(N):
        threads.append(Thread(customer, customerId, helper))

    for t in threads:
        t.join()

if __name__ == "__main__":
    """
    Entry point of program
    """
    main()