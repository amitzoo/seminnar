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

def merge(left, right):
    ret = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] < right[ri]:
            ret.append(left[li])
            li += 1
        else:
            ret.append(right[ri])
            ri += 1

    if (li == len(left)):
        ret.extend(right[ri:])
    else:
        ret.extend(left[li:])
    return ret


def mergesort(lyst):
    if len(lyst) <= 1:
        return lyst
    ind = len(lyst) // 2        # The floor division // rounds the result down to the nearest whole number
    return merge(mergesort(lyst[:ind]), mergesort(lyst[ind:]))


def mergeSortThreadParallel(lyst, conn, num_of_proc, lock):

    if num_of_proc.value <= 1 or len(lyst) <= 1:
        conn.send(mergesort(lyst))
        conn.close()
        return

    ind = len(lyst) // 2

    with lock:
        num_of_proc.value -= 1

    pconnLeft, cconnLeft = Pipe()
    leftProc = threading.Thread(target=mergeSortThreadParallel, args=(lyst[:ind], cconnLeft, num_of_proc, lock))

    leftProc.start()

    with lock:
        num_of_proc.value -= 1

    pconnRight, cconnRight = Pipe()
    rightProc = threading.Thread(target=mergeSortThreadParallel, args=(lyst[ind:], cconnRight, num_of_proc, lock))

    rightProc.start()

    conn.send(merge(pconnLeft.recv(), pconnRight.recv()))
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

    chunks = [lyst[x:x + sub_list_length] for x in range(0, len(lyst)-1, sub_list_length)]
    if diff > 0:
        chunks[len(chunks) - 1] += lyst[-diff:]  # Add the remaining numbers after the subdivision to sub-lists

    if thread_or_process == 2:         # Processes
        pool = multiprocessing.Pool(processes=num_of_proc)
        result = pool.map(mergesort, chunks)

        if len(result) == 1:
            lyst = result[0]
        else:
            lyst = merge(result[0], result[1])
            for x in range(2, len(result), 1):
                lyst = merge(lyst, result[x])

    else:                                   # Threads
        pconn, cconn = Pipe()
        lock = threading.Lock()
        num_of_proc = multiprocessing.Value('i', num_of_proc)
        p = threading.Thread(target=mergeSortThreadParallel, args=(lyst, cconn, num_of_proc, lock))
        p.start()
        lyst = pconn.recv()
        p.join()

    total_time = time.perf_counter() - start_time

    if isSorted(lyst):
        print("Finish sort")
    else:
        print('mergeSortParallel did not sort. oops.')

    return total_time, lyst[:50]