### Student: Matej Chvostek

# Overview
In this branch you can find our solution for the [7th assigment](https://uim.fei.stuba.sk/i-ppds/7-cvicenie/).

## Task
We have to implement at least 3 coroutines and a scheduler, which manages these coroutines.

## Solution

We have `main()` function, where are 3 coroutines created as instances of `coroutine()`. Their identifiers are `2`, `5` and `8`.
This is because we generate in scheduler function `scheduler()` random numbers in range `(0, 10)`, meanwhile **scheduler**
selects that coroutine, whom **identifier** is the closest to generated number. Then the selected coroutine receives a number
from the scheduler and prints it.

So the selection is as follows:
- *coroutine* with `id=2` can receive [`1, 2, 3`].
- *coroutine* with `id=5` can receive [`4, 5, 6`].
- *coroutine* with `id=8` can receive [`7, 8, 9`].

Program stops when the **sum** of the generated numbers is more than **60**.

## Program output
```
I'm now running. My id is 2
I'm now running. My id is 5
I'm now running. My id is 8
coroutine 5: received 6, possible values [4, 5, 6]
coroutine 2: received 2, possible values [1, 2, 3]
coroutine 5: received 4, possible values [4, 5, 6]
coroutine 5: received 6, possible values [4, 5, 6]
coroutine 5: received 5, possible values [4, 5, 6]
coroutine 2: received 1, possible values [1, 2, 3]
coroutine 2: received 3, possible values [1, 2, 3]
coroutine 5: received 4, possible values [4, 5, 6]
coroutine 5: received 6, possible values [4, 5, 6]
coroutine 2: received 2, possible values [1, 2, 3]
coroutine 5: received 5, possible values [4, 5, 6]
coroutine 2: received 3, possible values [1, 2, 3]
coroutine 8: received 9, possible values [7, 8, 9]
coroutine 2: received 1, possible values [1, 2, 3]
coroutine 8: received 9, possible values [7, 8, 9]
I'm now quitting. My id is 2
I'm now quitting. My id is 5
I'm now quitting. My id is 8
```

We can see, that coroutines are called correctly. Order of the coroutines is randomized and they are stopped from the
scheduler when the sum is **66**.


