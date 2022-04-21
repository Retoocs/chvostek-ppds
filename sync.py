import time

def task(sleepTime):
    print(f"Evaluating task for estimated {sleepTime} seconds.")
    time.sleep(sleepTime)
    print("Task finished")


def main():
    tasks = [(task, 3), (task, 4), (task, 5)]

    start = time.time()
    for t, l in tasks:
        t(l)
    print(f"Elapsed time: {time.time() - start:.2f} sec")


if __name__ == "__main__":
    main()