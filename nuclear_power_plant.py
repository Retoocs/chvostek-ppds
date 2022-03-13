from random import randint
from time import sleep

from fei.ppds import Mutex, Semaphore, Event, Thread, print

class Lightswitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()

class SimpleBarrier(object):
    """
    A synchronization object of kind barrier
    """
    def __init__(self, n):
        """
        Initialization method
        :param n: represents number of threads
        """
        self.numberOfThreads = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
        Main method of barrier object. Threads wait in this function to continue
        :return: none
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.numberOfThreads:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()

class SychronizationHelper(object):
    def __init__(self, nWriters):
        self.accessData = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_monitor = Lightswitch()
        self.ls_sensor = Lightswitch()
        self.validData = Event()
        self.barrier = SimpleBarrier(nWriters)

def monitor(monitorId, sh):
    sh.validData.wait()
    while True:
        sh.turnstile.wait()
        sh.turnstile.signal()
        numberOfReadingMonitors = sh.ls_sensor.lock(sh.accessData)
        readTime = randint(40, 50) / 1000
        print("monitor %02d: number_of_reading_monitors=%02d, read_time=%02d ms" % (monitorId, numberOfReadingMonitors, readTime*1000))
        sleep(readTime)
        sh.ls_sensor.unlock(sh.accessData)



def sensor(sh, minWait, maxWait, type):
    sleep(randint(50, 60) / 1000)
    writeTime = randint(minWait, maxWait) / 1000
    sleep(writeTime)
    print(f"Writing data... [{type}]")
    sh.barrier.wait()
    sh.validData.signal()
    while True:
        sleep(randint(50, 60) / 100)
        sh.turnstile.wait()
        numberOfWritingSensors = sh.ls_monitor.lock(sh.accessData)
        sh.turnstile.signal()
        writeTime = randint(minWait, maxWait) / 1000
        print("sensor %s: number_of_writing_sensors=%02d, write_time=%02d ms" % (type, numberOfWritingSensors, writeTime*1000))
        sleep(writeTime)
        sh.ls_monitor.unlock(sh.accessData)



if __name__ == "__main__":
    helper = SychronizationHelper(3)
    Thread(sensor, helper, 10, 20, "P")
    Thread(sensor, helper, 10, 20, "T")
    Thread(sensor, helper, 20, 25, "H")

    threads = [Thread(monitor, i, helper) for i in range(8)]
    [t.join() for t in threads]