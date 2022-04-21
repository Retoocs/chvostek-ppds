"""
Authors: Mgr. Ing. Matúš Jókay, PhD., Bc. Matej Chvostek
University:  Slovak University of Technology in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/
"""

import asyncio
import time

async def task(sleepTime):
    """
    Function to simulate some task. For simulation sleep() function is used.
    :param sleepTime: delay in second for sleep()
    :return: None
    """
    print(f"Evaluating task for estimated {sleepTime} seconds.")
    await asyncio.sleep(sleepTime)
    print("Task finished")


async def main():
    """
    Main function. Asynchronously starts tasks with params
    :return:
    """
    start = time.time()
    await asyncio.gather(
        task(3),
        task(4),
        task(5),
    )
    print(f"Elapsed time: {time.time() - start:.2f} sec")


if __name__ == "__main__":
    """
    Entry point of program
    """
    asyncio.run(main())