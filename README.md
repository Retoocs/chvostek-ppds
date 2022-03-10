## Student: Matej Chvostek
# Overview
In this branch you can find our solution for the [4th assigment](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/).

## Long story short
This assigment simulates a part of nuclear power plant things. We have **3 different sensors**, which **write** data and we have **8 monitors**, that **read** written data.
Multiple sensors and multiple monitors can write or read data **at the same time**, but monitor cannot read when some data are being written by the sensor. On the other hand a sensor
cannot write a data when data are being read by the monitor. Each sensor has it's own duration to write data and repetition time `50-60ms`. Monitors repeat reading at no time.

Another condition is, that at the start monitor can read only if every of the 3 sensors have written some data.

## Analysis
We have 2 categories of processes: `monitors` and `sensors`. We cannot have situation where monitor **reads** the data and sensor **writes** the data at the same time.
So we have to use 2 light switches for each category.

Since monitors repeat reading in no time, we have to ensure, that a sensor can also write. We don't want a sensor-starvation. We can use a `turnstile` to prioritize sensors.

To make at the beginning, that a monitor will read only if every sensor have written data, we can use a barrier with the event after the barrier. This will signal, that
every sensor have written some data, so monitors can start reading them.

So overall we will use **2 light switches, turnstile, barrier and event**.

## Pseudocode
```python
for i in range(3):
    create_and_run_thread(sensor)
for i in range(8):
    create_and_run_thread(monitor)
```

```python
def sensor():
    sleep(50-60ms)
    sleep_as_write(10-20ms or 20-25ms)
    barrier.wait()
    event.signal()
    while True:
        sleep(50-60ms)
        turnstile.wait()
        ls_monitor(accessData).lock()
        turnstile.signal()
        sleep_as_write(10-20ms or 20-25ms)
        ls_monitor(accessData).unlock()
```

```python
def monitor():
    event.wait()
    while True:
        turnstile.wait()
        turnstile.signal()
        ls_sensor(accessData).lock()
        sleep(40-50ms)
        ls_sensor(acessData).unlock()
```

## Implementation

## Conclusion