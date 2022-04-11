import random
import math
import time

def coroutine(id):
    try:
        print(f"I'm now running. My id is {id}")
        while True:
            i = (yield)
            print(
                f"coroutine {id}: received {i}, possible values [{id - 1}, {id}, {id + 1}]")
    except:
        print(f"I'm now quitting. My id is {id}")

def scheduler(coroutines):
    count = len(coroutines)
    total = 0
    while total < count * 20:
        time.sleep(0.2)
        randNum = random.randint(1, 9)
        idx = math.floor((randNum - 1) / count)
        coroutines[idx].send(randNum)
        total += randNum

    for c in coroutines:
        c.close()

def main():
    ids = [2, 5, 8]

    c2 = coroutine(ids[0])
    c5 = coroutine(ids[1])
    c8 = coroutine(ids[2])

    coroutines = [c2, c5, c8]
    for c in coroutines:
        next(c)

    scheduler(coroutines)

if __name__ == "__main__":
    main()