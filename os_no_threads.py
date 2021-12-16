# Ενότητα 14.6 Πολυπρογραμματισμός
# παράδειγμα χωρίς threads

import time
import sys

task = sys.argv[-1]

def task1():
    time.sleep(.5)

def task2():
    for i in range(10000):
        x = (i, i**2, i**i)

def do_work(item):
    if task == "sleep":
        task1()
    elif task == "cpu":
        task2()

start = time.perf_counter()
for item in range(5):
    do_work(item)
print('\nΣυνολικός χρόνος εκτέλεσης των 5 εργασιών: {:.4f}'.format(time.perf_counter() - start))
