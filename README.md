# Overview
In this branch you can find our solution for the [5th assigment](https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/).

## Long story short
In this problem we have savages and cooks in the tribe. Savages take and eat portions from the pot and cooks make the portions and put them into the pot. 

**There are several rules:**
- If a savage detects empty pot, he wakes up every cook in the tribe.
- If cooks are woken up, portions are made simultaneously.
- A savage can continue taking portions only if the pot has been refilled.
- Only one of the cooks can signal, that a pot has been refilled with portions.

## Analysis
So we have 2 sides of the problem: savage's and cook's.

Savage takes and eats portions in a loop. Before taking a portion, he must check if the pot contains any. Otherwise he signals, that the pot is empty and every savage waits. He signals `C-times`, so
`C` cooks can start cooking, since we use a `semaphore`.
We can lock checking and taking with a mutex. So when a savages waits for the pot getting refilled, other savages wait at the `mutex.lock()`.

Cook waits for the semaphore signal, that pot is empty in a loop. After the signal he makes the portions. Since in our solution a cook cooks `M` portions, where `M` is capacity of the pot, he can
put portions only if there is `0` portions in the pot. So before he puts portions, he must check, that a pot contains `0` portions. We have to do this under the `mutex` because it can happen, that he checks there is `0` portions
and meanwhile someone else fulfills the pot. But we have to use different mutex than a savages holds, because we'd have a **deadlock**. Once the portions are put, we can `unlock` the mutex. 
To make only one of the cooks can signal refillment of the pot, at the end we implement a `barrier`, where the last thread signals for the savage. However we have to use 2 barriers since we use them
in a loop.

## Pseudocode
```python
def getServingFromPot():
    servings -= 1

def savage():
    while True:
        mutex1.lock()
        if servings == 0:
            emptyPot.signal(C)
            fullPot.wait()
        getServingFromPot()
        mutex1.unlock()
 
        eat()
```

```python
def putServingsInPot():
    servings += M
 
def cook():
    while True:
        emptyPot.wait()
        portions = make_portions()
        mutex2.lock()
        if servings == 0:
            putServingsInPot(portions)
        mutex2.unlock()
        
        barrier1.wait()
        barrier2.wait(last_thread_signal_pot_is_full=True)        
```
```python
def main():
    mutex = Mutex()
    servings = 0
    fullPot = Semaphore(0)
    emptyPot = Semaphore(0)
    
    barrier1 = SimpleBarrier()
    barrier2 = SimpleBarrier()

    for savage_id in [0, 1, 2, ..., N-1]:
        create_and_run_thread(savage, savage_id)
    for cook_id in [0, 1, 2, ..., C-1]:
        create_and_run_thread(cook, cook_id)
```

## Implementation
Our implementation is pretty much the same as we have in pseudocode. We have added some printings and initializations. It works as we intended.

Here's an example of **program output** *(savages=3, pot-capacity=2, cooks=5)*:
```
savage  0: portions left in pot:  0
savage  0: waking up cooks
cook    0: cooking
cook    1: cooking
cook    2: cooking
cook    3: cooking
cook    4: cooking
cook    2: inserting portions
savage  0: taking a portion
savage  0: eating
savage  1: portions left in pot:  1
savage  1: taking a portion
savage  1: eating
savage  2: portions left in pot:  0
savage  2: waking up cooks
cook    4: cooking
cook    2: cooking
cook    1: cooking
cook    3: cooking
cook    0: cooking
cook    2: inserting portions
savage  2: taking a portion
savage  2: eating
savage  2: portions left in pot:  1
savage  2: taking a portion
savage  2: eating
savage  0: portions left in pot:  0
savage  0: waking up cooks
cook    3: cooking
cook    4: cooking
cook    1: cooking
cook    0: cooking
cook    2: cooking
cook    1: inserting portions
savage  0: taking a portion
...
```

At the start pot is empty. First savage wakes up cooks. Every cook cooks and only one of them puts the portions into the pot. Then a savage, who waits, takes a portion. Then other savages take portions
until the pot is empty again.