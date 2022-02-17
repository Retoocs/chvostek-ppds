from collection.Collection import Counter
from fei.ppds import Thread

class Shared():
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size

def do_count(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1

shared = Shared(1000000)
t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)
t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())
