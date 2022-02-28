# Implementation of barriers
## Overview
The assignment consists of two sub-problems. In the **first** problem we have to implement simple barrier by using synchronization object `Event` from `fei.ppds`.
The **second** problem is to implement the barrier from the **first** problem, but it must be **reusable**.

The logic behind a synchronization object of type `Event` is, that it holds the thread in it's method `wait()` until the event is set by calling method `signal()` or `set()`.
Then is every thread released if it's using the same instance of `Event`.

## Solution of the first problem
### Description
In this problem we don't have to implement reusable barrier. So we don't bother to write down anywhere the `clear()` method, which resets the *event*.

### Implementation
Our barrier is represented by class `SimpleBarrier`.  Threads are held in method `wait()`. If a thread enters the method, it increments the **counter** by 1.
The last thread, that entered the method sets counter to 0 and signals the event. After that, every thread is released.

To confirm the implementation, we simulated the use of barrier in function `barrier_example()`.

```python
class SimpleBarrier:
    def __init__(self, n):
        self.numberOfThreads = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.numberOfThreads:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()
```


## Solution of the second problem
### Description
In this problem we have to implement reusable barrier, that is implemented by **events**. We can use the barrier from the solution 1, but this barrier must consists of `clear()` method as well to reset the event, so it can be reused.

The assignment's condition is, that every thread should wait before *rendezvous* section and before *critical* section. 
```python
for i in range(ITERATIONS):
    rendezvous()
    critical_area()
```

**Rendezvous** section is represented by function `rendezvous()` and **critical** section by `critical_area()`.

### Implementation
The first attemp to solve this was to use the barrier from the 1st problem, but with the `clear()` at the end:
```python
def wait(self):
    self.mutex.lock()
    self.counter += 1
    if self.counter == self.numberOfThreads:
        self.counter = 0
        self.event.set()
    self.mutex.unlock()
    self.event.wait()
    self.event.clear()
```
The idea is to clear the event after threads are released. We didn't find it wrong, that `clear()` is called multiple times. It worked pretty well. Threads were in the correct order,
until we decided to put random sleep instruction after `mutex.unlock()`. We simulated, that last released the mutex, but wasn't able to continue,
so another thread took the place in execution. That another thread executes `clear()`. It means, that the last thread didn't manage to pass the
`wait()` instruction in time. Deadlock appears.

In the second attemp we use the `clear()` method at the beginning of the `wait()` method. The idea is straight. If we want to reuse the barrier, we have to clear the event. So we do it at the beginning.
This seems to work well.

```python
def wait(self):
    self.event.clear()
    self.mutex.lock()
    self.counter += 1
    if self.counter == self.numberOfThreads:
        self.counter = 0
        self.event.set()
    self.mutex.unlock()
    self.event.wait()
```

Another problem to solve is whether we use 1, 2 or 3 different instances of `SimpleBarrier` in loop. First of all we have tu put barrier before
`rendezvous()` and `critical_area()` and also at the end of the loop. If we don't put barrier at the end of loop, the thread, which have just executed
`critical_area()` would have afterwards execute `before_rendezvous()`. This we do not want to happen.

Logicly we want to use either 1 different instance or 3 different instances of `SimpleBarrier`. With the implementation of `SimpleBarrier.wait()` we have, we are not able to use only 1 different instance.
Because it can happen, that the last thread sets the event and doesn't reach the `wait()`, meanwhile another thread executes `clear()`.
So the previous thread is **locked-in** and the deadlock appears.

**Final working solution:**
```python
def barrier_example(sb1, sb2, sb3, thread_name):
    ITERATIONS = 5
    for i in range(ITERATIONS):
        before_rendezvous(thread_name)
        sb1.wait()
        rendezvous(thread_name)
        sb2.wait()
        critical_area(thread_name)
        sb3.wait()
```

