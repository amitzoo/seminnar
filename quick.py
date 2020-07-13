from multiprocessing import Pipe
import threading
import multiprocessing
import random, time
import Person


def init_list(obj_or_int, list_size, lyst):
    if obj_or_int == 'o' or obj_or_int == 'O':
        for x in range(list_size):
            height_random = random.choice(range(100, 200))
            weight_random = random.choice(range(20, 100))
            age_random = random.choice(range(20, 120))
            lyst.append(Person.Person(height_random, weight_random, age_random))
    else:
        lyst = random.sample(range(list_size*2), list_size)
    return lyst

def quicksort(lyst):
    if len(lyst) <= 1:
        return lyst
    pivot = lyst.pop(random.randint(0, len(lyst) - 1))
    return quicksort([x for x in lyst if x < pivot]) + [pivot] + quicksort([x for x in lyst if x > pivot])

'''def quicksortParallel(lyst, conn):

    if num_of_proc.value <= 1 or len(lyst) <= 1:
        conn.send(quicksort(lyst))
        conn.close()
        return

    pivot = lyst.pop(random.randint(0, len(lyst) - 1))

    with lock:
        num_of_proc.value -= 1

    leftSide = [x for x in lyst if x < pivot]  # change the name of class attribute here
    rightSide = [x for x in lyst if x > pivot]  # change the name of class attribute here

    pconnLeft, cconnLeft = Pipe()
    leftProc = Process(target=quicksortParallel, args=(leftSide, cconnLeft))

    leftProc.start()

    with lock:
        num_of_proc.value -= 1

    pconnRight, cconnRight = Pipe()
    rightProc = Process(target=quicksortParallel, args=(rightSide, cconnRight))


    rightProc.start()

    conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
    conn.close()

    leftProc.join()
    rightProc.join()
'''

def quicksortThreadParallel(lyst, conn, num_of_proc, lock):

    if num_of_proc.value <= 1 or len(lyst) <= 1:
        conn.send(quicksort(lyst))
        conn.close()
        return

    pivot = lyst.pop(random.randint(0, len(lyst) - 1))

    with lock:
        num_of_proc.value -= 1

    leftSide = [x for x in lyst if x < pivot]
    rightSide = [x for x in lyst if x > pivot]

    pconnLeft, cconnLeft = Pipe()
    leftProc = threading.Thread(target=quicksortThreadParallel, args=(leftSide, cconnLeft, num_of_proc, lock))

    leftProc.start()

    with lock:
        num_of_proc.value -= 1

    pconnRight, cconnRight = Pipe()
    rightProc = threading.Thread(target=quicksortThreadParallel, args=(rightSide, cconnRight, num_of_proc, lock))

    rightProc.start()

    conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
    conn.close()

    leftProc.join()
    rightProc.join()

def isSorted(lyst):
    """
    Return whether the argument lyst is in non-decreasing order.
    """
    # Cute list comprehension way that doesn't short-circuit.
    # return len([x for x in
    #            [a - b for a,b in zip(lyst[1:], lyst[0:-1])]
    #            if x < 0]) == 0
    for i in range(1, len(lyst)):
        if lyst[i] < lyst[i - 1]:
            return False
    return True

def start_sort(num_of_proc, obj_or_int, list_size, thread_or_process):
    start_time = time.perf_counter()

    result = []
    sub_list_length = list_size // num_of_proc
    diff = list_size % num_of_proc

    lyst = list()
    lyst = init_list(obj_or_int, list_size, lyst)

    chunks = [lyst[x:x + sub_list_length] for x in range(0, len(lyst) - 1, sub_list_length)]
    if diff > 0:
        chunks[len(chunks) - 1] += lyst[-diff:]  # Add the remaining numbers after the subdivision to sub-lists

    if thread_or_process == 2:                          # Processes
        pool = multiprocessing.Pool(processes=num_of_proc)
        result = pool.map(quicksort, chunks)
        lyst = result[0]

    else:
        pconn, cconn = Pipe()
        lock = threading.Lock()
        num_of_proc = multiprocessing.Value('i', num_of_proc)
        p = threading.Thread(target=quicksortThreadParallel, args=(lyst, cconn, num_of_proc, lock))
        p.start()
        lyst = pconn.recv()
        p.join()

    total_time = time.perf_counter() - start_time

    if isSorted(lyst):
        print("Finish to sort")
    else:
        print('quickSortParallel did not sort. oops.')

    return total_time, lyst[:50]