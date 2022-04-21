### Student: Matej Chvostek

# Overview
In this branch you can find our solution for the [8th assigment](https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/).

## Task
We have to implement simple demonstration between **synchronous** and **asynchronous** program.

## Solution

For our demonstration we have chosen simple program, that has `main()`, which calls `task()` function. This `task()` function consists of `sleep()` as blocking instruction. In **asynchronous** version
we use library `asyncio` for `sleep` and `gather` in the `main()` function.

## Program output

### Synchronous version
```
Evaluating task for estimated 3 seconds.
Task finished
Evaluating task for estimated 4 seconds.
Task finished
Evaluating task for estimated 5 seconds.
Task finished
Elapsed time: 12.00 sec
```
We can see, that this simple program behave as expected. Total elapsed time is equal to `3 + 4 + 5` seconds.
### Asynchronous version
```
Evaluating task for estimated 3 seconds.
Evaluating task for estimated 4 seconds.
Evaluating task for estimated 5 seconds.
Task finished
Task finished
Task finished
Elapsed time: 5.00 sec
```
In the **asynchronous** version the total elapsed time is equal to time of the task, that has the biggest delay. It's because the blocking instruction `sleep()` is now no longer blocking instruction.


