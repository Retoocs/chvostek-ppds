# Implementation of synchronized Fibonacci sequence
## Overview

The goal of this task is to compute *Fibonacci sequence* by multiple threads. We must also ensure, that the computation starts only if every thread is created.
Each thread should compute one element of sequence. We have to show implementation of using `Semaphores` and `Events`.

## Implementation
To achieve, that every thread is created and then computation starts, we can use a barrier. 

Our class `SynchronizationHelper` represents a barrier.
`SynchronizationHelper` consists of method `wait_for_creation()`, which is actual method for barrier and is called at the beginning of function
`compute_fibonacci()`. It is independent from application logic or wait method whether we use `Event` or `Semaphore` as synchronization object inside our helper class.

Once the threads are gathered at the barrier, they start to compute actual elements of *fibonacci sequence* one by one. The problem here is, that
we must compute each element one by one, from start to end. This we ensure by using global mutex (*created in entry point of program*) and shared index counter (*an attribute of class `SynchronizationHelper`*).

```python
def compute_fibonacci(sh, mutex):
    print("before wait")
    # method of barrier
    sh.wait_for_creation()
    # one by one thread execution
    mutex.lock()
    fib_seq[sh.indexCounter+2] = fib_seq[sh.indexCounter] + fib_seq[sh.indexCounter+1]
    sh.indexCounter += 1
    mutex.unlock()
```

## Conclusion
Our solution is not one of the greatest, but it accepts the meets of this assignment. There are many other ways how to solve it.

### Other solution no. 1
We could implement, that threads come to barrier in random order, but continue in ascending order by their `thread_id` starting from 0 one by one. This `thread_id`
would represent an index into *Fibonacci sequence*. How to implement such solution? In wait method of barrier we can use a local variable of type `Event` or `Semaphore`
, so each thread would have it's own synchronization object. These objects would be mapped in some collection. For example a map (in Python: *dictionary*). After barrier we 
can release them by their `thread_id` as we want by setting event or signaling a semaphore.

### Other solution no. 2
This solution doesn't meet the assigment conditions well, but it's interesting and simple (maybe not effective). It uses 0 synchronization objects.

The idea is something like this:
```python
def compute_fibonacci(i):
    if previous two elements are zeros:
        wait in loop until they are not zeros
    else:
        compute the element by previous two elements
```

However this doesn't meet the condition, that it should compute after every thread is created. It might happen so or might not.

### What is the smallest number of synchronization objects used?
In my main solution, which meets the assigment are total of 3 synchronization objects. In `Other solution no. 2` there is zero synchronization objects.