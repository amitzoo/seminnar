import functools
from functools import partial
from multiprocessing import Process, Pipe, Value, Pool, Queue
import threading
import multiprocessing
import random, time


# Python program for implementation of MergeSort

def mergeSort2(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        mergeSort2(L)  # Sorting the first half
        mergeSort2(R)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr


def merge(left, right, id):
    # print("proc {} start merge()".format(id))
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
    # conn.send(ret)
    # print("proc {} finish merge()".format(id))
    return ret


def mergesort(lyst, id):
    # print("proc {} start mergesort()".format(id))
    if len(lyst) <= 1:
        # conn.send(lyst)
        return lyst
    ind = len(lyst) // 2  # The floor division // rounds the result down to the nearest whole number
    return merge(mergesort(lyst[:ind], id), mergesort(lyst[ind:], id), id)

def mergeSortParallel(lyst):

    sub_list_length = list_size // num_of_proc
    diff = list_size % num_of_proc

    chunks = [lyst[x:x + sub_list_length] for x in range(0, len(lyst) - 1, sub_list_length)]

    if diff > 0:
        chunks[len(chunks) - 1] += lyst[-diff:]

    pool.map(mergeSortParallel, lyst)

    return [mergesort(chunk, id) for chunk in chunks]


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
    list_size = 100000
    obj_or_int = 'i'
    lyst = random.sample(range(list_size*2), list_size)
    pool = Pool(processes=num_of_proc)
    start_time = time.perf_counter()
    total_time = 0



    processes_list = list()
    pipes_list = list()
    # result = []
    # mergeSortParallel(chunks)
    result = mergeSortParallel(lyst, list_size, num_of_proc)
    # result = pool.map(mergeSortParallel, lyst, list_size, num_of_proc)
    print("result", result)
    lyst = result
    # if len(result) == 1:
    #     lyst = result[0]
    # else:
    #     lyst = merge(result[0], result[1], 0)
    #     for x in range(2, len(result), 1):
    #         lyst = merge(lyst, result[x], 0)


    total_time = time.perf_counter() - start_time
    print (total_time)
    if isSorted():
        print("\n\n", lyst)
        print("\n\n", len(lyst))
    else:
        print('mergeSortParallel did not sort. oops.')


