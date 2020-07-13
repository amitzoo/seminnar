import functools
from functools import partial
from multiprocessing import Process, Pipe, Value, Pool, Queue
import threading
import multiprocessing
import random, time


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

    if li == len(left):
        ret.extend(right[ri:])
    else:
        ret.extend(left[li:])
    return ret


def mergesort(lyst):
    if len(lyst) <= 1:
        return lyst
    ind = len(lyst) // 2  # The floor division // rounds the result down to the nearest whole number
    return merge(mergesort(lyst[:ind]), mergesort(lyst[ind:]))

def mergeSortParallel(lyst):
    return mergesort(lyst)


lyst = list()

def isSorted():
    global lyst
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

if __name__ == '__main__':

    num_of_proc = 16
    list_size = 1000000
    obj_or_int = 'i'
    lyst = random.sample(range(list_size*2), list_size)
    pool = Pool(processes=num_of_proc)
    start_time = time.perf_counter()
    total_time = 0

    sub_list_length = list_size // num_of_proc
    diff = list_size % num_of_proc

    chunks = [lyst[x:x + sub_list_length] for x in range(0, len(lyst) - 1, sub_list_length)]

    if diff > 0:
        chunks[len(chunks) - 1] += lyst[-diff:]


    processes_list = list()
    pipes_list = list()
    result = []
    # mergeSortParallel(chunks)
    result = pool.map(mergeSortParallel, chunks)




    lyst = list()

    if len(result) == 1:
        lyst = result[0]
    else:
        lyst = merge(result[0], result[1])
        for x in range(2, len(result), 1):
            lyst = merge(lyst, result[x])


    total_time = time.perf_counter() - start_time
    print(total_time)
    if isSorted():
        # print("\n\n", lyst)
        # print("\n\n", len(lyst))
        pass
    else:
        print('mergeSortParallel did not sort. oops.')


