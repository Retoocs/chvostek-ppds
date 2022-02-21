# Overview
In this branch you can find my solutions for the first assignment. There are total of 3 solutions, each in one .py file. 
Named:
- first_variant.py
- second_variant.py
- third_variant.py

## Program description
This program creates an instance of class Shared. An object Shared contains 3 attributes such as:
- an array called `elms`, initialized to `zeros`
- the ending index called `end`
- a counter, which we can understand as a pointer to the `elms`

Then program loops the array of object Shared and increments every element by one.

## Assignment problem
The problem in this task is, that we should use 2 threads in this program. This means we have competitive access in our shared object. We should try to fix this by using mutex.

## Notes
Each solution was developed with **Python v3.8**.

## Solutions
The idea behind each solution is to evaluate counter and element of array incrementations atomically.
### First solution (first_variant.py)
In the first solution we lock the mutex inside the while loop, but before the condition. We lock it here, because if we don't do that and put the `mutex.lock()` after the condition, we'd get a problem:
*Our program is in position to increment the last element. Thread `A` checks the condition, continues, increments the element and the counter. Meanwhile thread `B` is waiting at the `mutex.lock()` after the condition. Thread `A` is finished and unlocks the mutex. Thread `B` continues, but the counter is already out of the array boundaries. So we get an exception thrown and every element incremented.* So that's why we lock the mutex before the condition. 

Then the second problems occurs and that's we have now a **deadlock**. The thread, which passed the condition and broke the loop, locked the mutex, but haven't unlocked it. Solution for this problem is to put `mutex.unlock()` inside the breaking-condition.

This solution should work for any length of the array.
### Second solution (second_variant.py)
In this solution we lock the mutex after condition. To do that, we have to fix the condition by counting down the `shared.end`, because the *second* problem we mentioned earlier. It works, but it's not a great solution. 

It means we assume, that the program will use exactly 2 threads. If we use 1 thread, it wouldn't increment the last element and if we use more than 2 thread, it could throw out of boundaries exception.

The second reason why it is not a great solution is, that if we have an array of 1 element, this element wouldn't get incremented ever.

### Third solution (third_variant.py)
In previous two solutions threads were switching each loop iteration. In this third solution we lock and unlock the mutex outside the loop. That means even if we have program, that uses 2 threads, only one thread will increment every element in the array. Second thread will execute the function `do_count`, but it will break the loop at the first iteration, since the counter is already out of the boundary.

However this solution is the fastest of them all. We assume it's because it doesn't have to execute such mutex locking/unlocking instructions.

