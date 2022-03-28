### Student: Matej Chvostek

# Overview
In this branch you can find our solution for the [6th assigment](https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/).

## Long story short
We have chosen a barber shop problem. In this problem we have a barber and customers. Customers want to take the haircut. Barber shop has small capacity and only 1 chair for cuts. If the waiting room
is full, customers go home and come back later. Customers take haircuts in order they came to the shop.

## Implementation
We have implemented pseudocode from the assigment. We simulate, that we have **1 barber**, who has **fixed number of customers**. These customers go to barber shop **randomized** time as it simulates
growth of hair. Implementation contains class SynchHelper, where are stored useful variables to solve our synchronization problem.

To solve **FIFO** problem of customers, we use `queue` collection. This particular queue is *thread-safe* implemented. It means, that we don't have to
use it under our mutex when accessing it.

Here's an example of **program output** *(customers=20, shop-capacity=3, barber's chairs=1)*:
```
Barber   0: waiting for customer
Customer 8: waiting for haircut
Customer 9: waiting for haircut
Customer 7: waiting for haircut
Customer 10: I'll come next time
Customer 11: I'll come next time
Barber   0: cutting...
Customer 8: getting haircut...
Barber   0: waiting for customer
Barber   0: cutting...
Customer 8: thanks
Customer 9: getting haircut...
Customer 17: I'll come next time
Barber   0: waiting for customer
Barber   0: cutting...
Customer 9: thanks
Customer 7: getting haircut...
Barber   0: waiting for customer
Customer 7: thanks
Customer 14: waiting for haircut
Barber   0: cutting...
Customer 14: getting haircut...
Customer 16: waiting for haircut
Barber   0: waiting for customer
Barber   0: cutting...
Customer 5: waiting for haircut
Customer 16: getting haircut...
Customer 14: thanks
Customer 1: I'll come next time
Customer 18: I'll come next time
Barber   0: waiting for customer
Barber   0: cutting...
Customer 0: waiting for haircut
Customer 4: I'll come next time
Customer 16: thanks
Customer 5: getting haircut...
Barber   0: waiting for customer
Barber   0: cutting...
Customer 0: getting haircut...
Customer 0: thanks
Customer 5: thanks
Barber   0: waiting for customer
Customer 12: waiting for haircut
Barber   0: cutting...
Customer 12: getting haircut...
Barber   0: waiting for customer
...
```

At the start *barber* is ready to make haircut. Few *customers* come in and few have to go home. Then *barber* does the haircut for *customer no.8*.
And so on.

We can see, that *customers* are done in right order. We have barber shop capacity of only **3** *customers* and there is total of **20** of them. Even the *barber* 
is pretty fast in making haircuts, some of the *customers* must go home due to full shop capacity.