"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/3-cvicenie-fibonacci-vypinac-p-k-c-z-%f0%9f%92%a1/?%2F
"""

from time import sleep
from fei.ppds import Mutex, Semaphore, Thread, print
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm

class Shared(object):
    """
    Shared object by the threads.

    Attributes:
        free - signals the storage has free space
        items - signals, that storage contains some item
        pCounter - number of created items
        itemCount - actual number of items in storage
    """
    def __init__(self, N):
        """
        Constructor of class Shared
        :param N: size of storage
        """
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)
        self.pCounter = 0
        self.itemCount = 0

def producer(shared, productionTime, insertTime):
    """
    Simulates creation of item and insertion into storage
    :param shared: synchronization helper
    :param productionTime: time-length of item creation
    :param insertTime: time-length of item insertion
    :return: none
    """
    while True:
        sleep(productionTime)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        shared.pCounter += 1
        shared.itemCount += 1
        sleep(insertTime)
        shared.mutex.unlock()
        shared.items.signal()

def consumer(shared, processingTime, takeTime):
    """
    Simulates itme taking from the storage and item processing
    :param shared: synchronization helper
    :param processingTime: time-length of item processing
    :param takeTime: time-length of taking item from storage
    :return: none
    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(takeTime)
        shared.mutex.unlock()
        shared.itemCount -= 1
        shared.free.signal(1)
        sleep(processingTime)

def plot_graph(x, y, z, xLabel, yLabel, zLabel):
    """
    Plots 3D graph
    :param x: 1d array of x values
    :param y: 1d array of y values
    :param z: 1d array of z values
    :param xLabel: x-axis label
    :param yLabel: y-axis label
    :param zLabel: z-axis label
    :return: none
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_zlabel(zLabel)
    surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0)
    fig.colorbar(surf)

    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(6))
    ax.zaxis.set_major_locator(MaxNLocator(5))

    fig.tight_layout()
    plt.show()


def evaluate_graph1():
    """
    Core logic logic of system with the analysis. Creates configuration of system,
    runs variable analysis on producent-consument logic.
    :return: none
    """
    x = []
    y = []
    z = []

    # fixed params: CONSUMERS_COUNT, WAREHOUSE_SIZE, PRODUCTION_TIME, WAREHOUSE_INSERT_TIME, WAREHOUSE_TAKE_TIME, TOTAL_RUNTIME
    # variable params: (x)PRODUCERS_COUNT, (y)PROCESSING_TIME, (z)PCS_PER_SECOND

    # constants
    CONSUMERS_COUNT = 10
    WAREHOUSE_SIZE = 30
    PRODUCTION_TIME = 0.02
    WAREHOUSE_INSERT_TIME = 0.002
    WAREHOUSE_TAKE_TIME = 0.002
    TOTAL_RUNTIME = 0.08

    # variables
    producersCount = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
    processingTimes = [0.005, 0.010, 0.015, 0.020, 0.025, 0.035, 0.040, 0.045, 0.050, 0.055]

    progressCounter = 0
    totalCombinations = len(producersCount) * len(processingTimes)
    for producerCount in producersCount:
        for processingTime in processingTimes:
            sum_pcs = 0
            print(f"Iteration no. [{progressCounter}/{totalCombinations}]")
            for _ in range(10):
                s = Shared(WAREHOUSE_SIZE)
                c = [Thread(consumer, s, processingTime, WAREHOUSE_TAKE_TIME) for _ in range(CONSUMERS_COUNT)]
                p = [Thread(producer, s, PRODUCTION_TIME, WAREHOUSE_INSERT_TIME) for _ in range(producerCount)]
                sleep(TOTAL_RUNTIME)
                s.finished = True
                s.items.signal(100)
                s.free.signal(100)
                [t.join() for t in c + p]
                sum_pcs += s.pCounter
                print(f"Pocet vyrobenych produktov {s.pCounter}. Stav skladu: {s.itemCount} pcs")
            print(f"x: {producerCount}; y: {processingTime}")
            print("..................................................")
            progressCounter += 1
            pcsPerSecond = (sum_pcs / 10) / TOTAL_RUNTIME
            x.append(producerCount)
            y.append(processingTime)
            z.append(pcsPerSecond)
    plot_graph(x, y, z, 'Number of producers', 'Processing time (consumer)', 'Number of products per second')


if __name__ == "__main__":
    """
    Entry point of the program. Calls the core function
    """
    evaluate_graph1()

