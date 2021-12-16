## Κεφάλαιο 14 Λειτουργικά Συστήματα
# ΠΡΟΣΟΜΟΙΩΣΗ ΕΤΑΙΡΙΑΣ ΤΑΧΥΜΕΤΑΦΟΡΩΝ (παράδειγμα επικοινωνίας και συγχρονισμού νημάτων μέσω αντικειμένων Queue και Event)

# η βιβλιοθήκη  threading επιτρέπει τη διαχείριση νημάτων (ελαφρών διεργασιών) - περιλαμβάνει την κλάση Event
# https://docs.python.org/3/library/threading.html?highlight=threading#module-threading
import threading

# η βιβλιοθήκη queue επιτρέπει την επικοινωνία μεταξύ νημάτων - Η κλάση Queue υλοποιεί μηχανισμούς κλειδώματος
# https://docs.python.org/3/library/queue.html?highlight=queue#module-queue
import queue

# https://docs.python.org/3/library/concurrent.futures.html
# concurrent.futures βιβλιοθήκη που επιτρέπει την ασύγχρονη κλήση συναρτήσεων  a high-level interface for asynchronously executing callables
import concurrent.futures

# Η βιβλιοθήκη logging επιτρέπει την καταγραφή συμβάντων, ιδιαίτερα όταν τρέχουν ασύγχρονα νήματα
# https://docs.python.org/3/howto/logging.html
import logging

import time
import random

### άσκηση: μελετήστε πώς επηρεάζει την απόδοση του συστήματος, η τροποποίηση των παραμέτρων STORE_SIZE, NO_COURIERS, TIME_OPEN
# η απόδοση του συστήματος μετριέται με δείκτες όπως: αριθμός εξυπηρετούμενων πελατών, ωράριο εργασίας, μέσος χρόνος αναμονής
# προτείνετε μηχανισμό για βελτιστοποίηση της λειτουργίας της επιχείρησης.

STORE_SIZE = 20  # Χρητικότητα αποθήκης
NO_COURIERS = 10 # πλήθος διανομέων
TIME_OPEN = 1 # προσομοίωση διάρκειας λειτουργίας της επιχείρησης (sec)

def producer(queue, event):
    """Εδώ οι πελάτες παραδίδουν τα δέματα. Αν η αποθήκη έχει γεμίσει, περιμένουν"""
    customers = 0
    waiting = 0
    while not event.is_set(): # ενόσω το μαγαζί είναι ανοικτό παραλαμβάνουμε δέματα
        message = random.randint(1, 101)
        t1 = time.perf_counter()
        queue.put(message)
        customers += 1
        wait = time.perf_counter()-t1
        logging.info(f"Ο πελάτης έστειλε δέμα: {message}, αναμονή = {wait:.5f}", )
        waiting += wait
    logging.info(f"Τερματισμός producer. Δεν δεχόμαστε πλέον δέματα, εξυπηρετήθηκαν {customers} πελάτες, μέση αναμονή: {waiting/customers:.5f}")

def consumer(queue, event, id):
    """Ο Courrier μοιράζει τα δέματα στους αποδέκτες."""
    count = 0
    t0 = time.perf_counter()
    while not event.is_set() or not queue.empty(): # όταν κλείσει το μαγαζί **και** αδειάσει η αποθήκη, σχολάμε
        message = queue.get()
        q = queue.qsize()
        time.sleep( random.random())
        logging.info(f"Το δέμα : {message} παραδόθηκε από {id} (δέματα στην αποθήκη={q}) ")
        count += 1
    workLoad = time.perf_counter() - t0
    logging.info(f"Τερματισμός consumer {id}. (σύνολο δεμάτων που παραδόθηκαν: {count},  ωράριο: {workLoad:.5f}")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    storage = queue.Queue(maxsize=STORE_SIZE) # το μέγεθος της αποθήκης της εταιρίας (ουρά FIFO)

    event = threading.Event() # μηχανισμός για επικοινωνία των νημάτων, όταν αυτό ενεργοποιηθεί θα ειδοποιηθούν τα αντίστοιχα νήματα
    # https://docs.python.org/3/library/threading.html?highlight=threading%20event#threading.Event

    with concurrent.futures.ThreadPoolExecutor(max_workers = NO_COURIERS + 1 ) as executor: # threads pool
        executor.submit(producer, storage, event)
        for _i in range(NO_COURIERS):
            executor.submit(consumer, storage, event, f"courrier {_i+1}")
        # η επιχείρηση είναι ανοικτή για ένα διάστημα ....
        time.sleep(TIME_OPEN) # χρόνος λειτουργίας
        # η επιχείρηση κλείνει...
        logging.info("Main: τερματισμός.")
        event.set() # γνωστοποίηση τερματισμού σε άλλα νήματα