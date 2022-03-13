from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Event, Thread, print

class Lightswitch(object):
    """
    A Lightswitch synchronization object. One instance per 1 process-category
    """
    def __init__(self):
        """
        Initialization method. Counter counts number of threads in 'room'
        """
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        """
        Locks the 'room'
        :param sem: base synchronization object of type Semaphore
        :return: Number of threads in 'room' when calling this method
        """
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        """
        Unlocks the 'room'
        :param sem: base synchronization object of type Semaphore
        :return: None
        """
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
    """
    Wraps all the synchronization objects for this program.
    """
    def __init__(self, nWriters):
        """
        Initialization of needed attributes
        :param nWriters: number of threads from category 'writers'
        """
        self.accessData = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_monitor = Lightswitch()
        self.ls_sensor = Lightswitch()
        self.validData = Event()
        self.barrier = SimpleBarrier(nWriters)

def monitor(monitorId, sh):
    """
    Simulates the monitor function. 'Readers' category. Less prioritized than sensor.
    :param monitorId: identifier of monitor
    :param sh: object of type SynchronizationHelper
    :return: None
    """
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
    """
    Simulates the sensor function. 'Writers' category. It has higher priority than monitor
    :param sh: object of type SynchronizationHelper
    :param minWait: minimal time in ms it takes to write data. Depends on sensor type.
    :param maxWait: maximal time in ms it takes to write data. Depends on sensor type.
    :param type: type of sensor
    :return: None
    """
    sleep(randint(50, 60) / 1000)
    writeTime = randint(minWait, maxWait) / 1000
    sleep(writeTime)
    print(f"Writing data... [{type}]")
    sh.barrier.wait()
    sh.validData.signal()
    while True:
        sleep(randint(50, 60) / 1000)
        sh.turnstile.wait()
        numberOfWritingSensors = sh.ls_monitor.lock(sh.accessData)
        sh.turnstile.signal()
        writeTime = randint(minWait, maxWait) / 1000
        print("sensor %s: number_of_writing_sensors=%02d, write_time=%02d ms" % (type, numberOfWritingSensors, writeTime*1000))
        sleep(writeTime)
        sh.ls_monitor.unlock(sh.accessData)



if __name__ == "__main__":
    """
    Entry point of program. Three threads for 'writers' and 8 threads for 'readers' are created
    """
    helper = SychronizationHelper(3)
    Thread(sensor, helper, 10, 20, "P")
    Thread(sensor, helper, 10, 20, "T")
    Thread(sensor, helper, 20, 25, "H")

    threads = [Thread(monitor, i, helper) for i in range(8)]
    [t.join() for t in threads]