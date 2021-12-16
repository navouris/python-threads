# Ενότητα 14.6 Προγραμματισμός με ελαφρές διεργασίες
# εκτελείται από γραμμή εντολών ως python os_thread.py cpu ή sleep
import threading
from queue import Queue
import time
import sys

NO_THREADS = 5 # πλήθος νημάτων

if len(sys.argv)> 1: task = sys.argv[1]
else: task = 'cpu'

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

# η ελαφρά διεργασία worker παίρνει ένα αντικείμενο από την ουρά και το επεξεργάζεται
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()
        
# δημιουργία ουράς q.
#main
q = Queue()
for i in range(NO_THREADS):
     t = threading.Thread(target=worker) # δημιουργείται ελαφρά διεργασία
     t.daemon = True  # .
     t.start()
# τοποθέτησε αντικείμενα για επεξεργασία στην ουρά (εδώ ακεραίους αριθμούς).
start = time.perf_counter()
for item in range(NO_THREADS):
    q.put(item)
q.join()       # block μέχρι να τελειώσουν όλες οι διεργασίες
print(f'\nΣυνολικός χρόνος εκτέλεσης {NO_THREADS} εργασιών: {time.perf_counter() - start:.4f}')