"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/7-cvicenie/
"""
import random
import math

def coroutine(id):
    """
    A coroutine, which receives and prints data. The instance can receive only
    [id - 1, id, id + 1] numbers.
    :param id: identifier of coroutine instance
    :return: None
    """
    try:
        print(f"I'm now running. My id is {id}")
        while True:
            i = (yield)
            print(f"coroutine {id}: received {i}, possible values "
                  f"[{id - 1}, {id}, {id + 1}]")
    except GeneratorExit:
        print(f"I'm now quitting. My id is {id}")

def scheduler(coroutines):
    """
    Schedules coroutines. Generates random integer and calls a coroutine with
    the identifier, which is the closest to generated number
    :param coroutines: list of coroutine instances
    :return: None
    """
    count = len(coroutines)
    total = 0
    while total < count * 20:
        randNum = random.randint(1, 9)
        idx = math.floor((randNum - 1) / count)
        coroutines[idx].send(randNum)
        total += randNum

    for c in coroutines:
        c.close()

def main():
    """
    Creates coroutine instances and calls scheduler for that instances.
    :return: None
    """
    ids = [2, 5, 8]

    c2 = coroutine(ids[0])
    c5 = coroutine(ids[1])
    c8 = coroutine(ids[2])

    coroutines = [c2, c5, c8]
    for c in coroutines:
        next(c)

    scheduler(coroutines)

if __name__ == "__main__":
    """
    Entry point of the program
    """
    main()