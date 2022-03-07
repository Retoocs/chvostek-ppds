## Student: Matej Chvostek

# Overview
In this branch you can find our solution for the third assignment. 

## Problem
We have a program, that illustrates **producent-consument** problem while multi-threading. This program consists of system parameters:
- count of consumers
- count of producers
- warehouse size
- production time
- warehouse insert time
- processing time
- warehouse take time
- total runtime

Our goal is to optimize these parameters to achieve the most effective **production per second**.

## Our solution
In our solution we mark as **variables** `count of producers` and `processing time`. Any other parameter we mark as a **constant**. 

**Our constants**:
```python
CONSUMERS_COUNT = 10
WAREHOUSE_SIZE = 30
PRODUCTION_TIME = 0.02
WAREHOUSE_INSERT_TIME = 0.002
WAREHOUSE_TAKE_TIME = 0.002
TOTAL_RUNTIME = 0.08
```

**Our variables**:
```python
producersCount = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
processingTimes = [0.005, 0.010, 0.015, 0.020, 0.025, 0.035, 0.040, 0.045, 0.050, 0.055]
```

We try every combination, total of 100 combinations. Then we plot the results.

```
X-axis = Number of producers
Y-axis = Processing time of consumer
Z-axis = Number of products per second
```

### Graph analysis

[<img alt="1st image" src="https://i.ibb.co/ypVJvTr/graph-2.png" width="800"/>](1)

On the first image we see, that more producers we have, more products are created per second.

<img src="https://i.ibb.co/KqxfFjZ/graph-3.png" width="800"/>

On the second image we can see points `A` and `B` and a `flat area` on the top of the graph. As expected point `A` has bigger value of `Z-axis` than
point `B`. It's because at the same number of the producers, point `A` has smaller item processing time than point `B`.

The more interesting is the area on the top of the graph. We assumed, that if we have more producers we can get more produced items per second. The fact it doesn't happen is,
that our warehouse capacity is full. We have too many producers, that can our warehouse handle. So basically producers **wait** until a consumer **takes** an item from the warehouse.

### Analysis results
As we could see on the graph, the one of the more effective configurations of our system is to have around **32 producers**. It's not effective to have more than that.


