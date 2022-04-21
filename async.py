import asyncio
import time

async def task(sleepTime):
    print(f"Evaluating task for estimated {sleepTime} seconds.")
    await asyncio.sleep(sleepTime)
    print("Task finished")


async def main():
    start = time.time()
    await asyncio.gather(
        task(3),
        task(4),
        task(5),
    )
    print(f"Elapsed time: {time.time() - start:.2f} sec")


if __name__ == "__main__":
    asyncio.run(main())