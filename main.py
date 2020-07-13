from quick import ParallelQuicksort
from merge import ParallelMergeSort
import random

from multiprocessing import Process, Pipe, cpu_count


if __name__ == '__main__':

    lyst = random.sample(range(100 * 2), 100)

    chunks = [lyst[x:x + 10] for x in range(0, len(lyst), 10)]
    print(len(chunks[0]))
    print(lyst)
    print(lyst[-4:])
    l = [1,2,3]
    l += lyst[-4:]
    print(l)
    '''
    thread_or_process =  input("Do you want to sort by Threads or Processes? (t - for threads, p - for processes)\n")

    while thread_or_process != 'p' and thread_or_process != 'P' and thread_or_process != 't' and thread_or_process != 'T':
        thread_or_process =  input("Invalid input! (t - for threads, p - for processes)\n")

    quick_or_merge = input("Which sort do you want to run? (q - for quick, m - for merge)\n")

    while quick_or_merge != 'q' and quick_or_merge != 'Q' and quick_or_merge != 'm' and quick_or_merge != 'M':
        quick_or_merge = input("Invalid input! (q - for quick, m - for merge)\n")

    object_or_integers = input("What do you want to sort? objects or integers array? (o - for objects, i - for integers)\n")
    while object_or_integers != 'o' and object_or_integers != 'O' and object_or_integers != 'i' and object_or_integers != 'I':
        object_or_integers = input("Invalid input! (o - for objects, i - for integers)\n")

    list_size = int(input("Please insert size of list:\n"))
    while list_size <= 0 or list_size is None:
        list_size = int(input("Invalid input! size must be greater than 0!\n"))

    if thread_or_process == 'p' or thread_or_process == 'P':            # Processes
        n = cpu_count()
        print("CPU count is: ", n)
        num_of_processes = int(input("Input number of processes:\n"))
        while num_of_processes < 1 or num_of_processes > 2*n:
            num_of_processes = int(input("Invalid input! number of processes must be between 1 - {}!\n".format(2*n)))

        if quick_or_merge == 'q' or quick_or_merge == 'Q':     # quick sort (processes)
            quick_sort = ParallelQuicksort(num_of_processes, object_or_integers, list_size, thread_or_process)
            quick_sort.start_sort()
        else:                                                   # merge sort (processes)
            merge_sort = ParallelMergeSort(num_of_processes, object_or_integers, list_size, thread_or_process)
            merge_sort.start_sort()

    else:                                                               # Threads
        num_of_threads = int(input("Input number of threads:\n"))
        while num_of_threads < 1:
            num_of_threads = input("Invalid input! number of threads must be greater than 0")

        if quick_or_merge == 'q' or quick_or_merge == 'Q':     # quick sort (threads)
            quick_sort = ParallelQuicksort(num_of_threads, object_or_integers, list_size, thread_or_process)
            quick_sort.start_sort()
        else:                                                   # merge sort (threads)
            merge_sort = ParallelMergeSort(num_of_threads, object_or_integers, list_size, thread_or_process)
            merge_sort.start_sort()
            
        '''





