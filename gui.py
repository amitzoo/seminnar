from tkinter import *
from multiprocessing import cpu_count
from tkinter import messagebox
import os
import datetime
import quick
import merge
from SortSequential import sort

'''
    1 - Thread
    2 - Process
    
    1 - Quick
    2 - Merge
    
    1 - Object
    2 - Integer
'''

def startApplication():
    num_of_threads = 0
    num_of_processes = 0
    sorted_list=list()
    thread_or_process = selected_t_p.get()
    quick_or_merge = selected_q_m.get()
    object_or_integers = selected_o_i.get()
    list_size = int(list_size_spin.get())

    details = str(datetime.datetime.now())

    if object_or_integers == 1:     # Objects
        object_or_integers = 'o'
        details += "\nObjects"
    else:                           # Integers
        object_or_integers = 'i'
        details += "\nIntegers"

    if thread_or_process == 1:      # Threads
        num_of_threads = int(num_of_threads_spin.get())
        details += "\nNumber of threads: {}".format(num_of_threads)
    else:                           # Processes
        num_of_processes = int(num_of_processes_spin.get())
        n = cpu_count()
        if num_of_processes < 1 or num_of_processes > 2*n:
            messagebox.showerror("Invalid input!", "number of processes must be between 1 - {}!\n".format(2*n))
            return
        details += "\nNumber of processes:{}".format(num_of_processes)
        details += "\nList size: {}".format(list_size)

    if thread_or_process == 2:            # Processes
        if quick_or_merge == 1:     # quick sort (processes)
            total_time, sorted_list = quick.start_sort(num_of_processes, object_or_integers, list_size, thread_or_process)
            # quick_sort.start_sort()
            details += "\nQuick Sort\nTotal Time:{:.2f}\nsorted list: {}".format(total_time, sorted_list)

        else:                       # merge sort (processes)
            total_time, sorted_list  = merge.start_sort(num_of_processes, object_or_integers, list_size, thread_or_process)
            # merge_sort = ParallelMergeSort(num_of_processes, object_or_integers, list_size, thread_or_process)
            # merge_sort.start_sort()
            details += "\nMerge Sort\nTotal Time:{:.2f}\nsorted list: {}".format(total_time, sorted_list)

    else:                                                               # Threads
        if quick_or_merge == 1:     # quick sort (threads)
            total_time, sorted_list  = quick.start_sort(num_of_threads, object_or_integers, list_size, thread_or_process)
            # quick_sort.start_sort()
            details += "\nQuick Sort\nTotal Time:{:.2f}\nsorted list: {}".format(total_time, sorted_list)

        else:                                                   # merge sort (threads)
            total_time, sorted_list  = merge.start_sort(num_of_threads, object_or_integers, list_size, thread_or_process)
            # merge_sort = ParallelMergeSort(num_of_threads, object_or_integers, list_size, thread_or_process)
            # merge_sort.start_sort()
            details += "\nMerge Sort\nTotal Time:{:.2f}\nsorted list: {}".format(total_time, sorted_list)

    details += " sec \n\n"
    with open(os.path.join(os.getcwd(),"output"), "w") as file:
        file.write(details)

def showGraph():
    list_size = int(list_size_spin2.get())
    s = sort(list_size)
    s.createGraph()

if __name__ == '__main__':
    window = Tk()
    window.wm_attributes("-topmost",1)
    window.title("Welcome to Seminar Sort World")

    #window.geometry('500x300')

    # Thread/Process
    thread_process_label = Label(text="Thread/Process:")
    selected_t_p = IntVar()
    thread_rad = Radiobutton(window, text='Thread', value='1', variable=selected_t_p)
    thread_rad.select()
    process_rad = Radiobutton(window, text='Process', value='2', variable=selected_t_p)

    # Quick/Merge
    quick_merge_lable = Label(text="Quick/Merge:")
    selected_q_m = IntVar()
    quick_rad = Radiobutton(window, text='Quick', value='1', variable=selected_q_m)
    quick_rad.select()
    merge_rad = Radiobutton(window, text='Merge', value='2', variable=selected_q_m)

    # Objects/Integers
    object_integer_label = Label(text="Objects/Integers:")
    selected_o_i = IntVar()
    object_rad = Radiobutton(window, text='Objects', value='1', variable=selected_o_i)
    integer_rad = Radiobutton(window, text='Integers', value='2', variable=selected_o_i)
    integer_rad.select()

    # List size
    list_size_label = Label(text="List size:")
    var = IntVar(value=1000)  # initial value
    list_size_spin = Spinbox(window, from_=1, to=1000000, width=15, textvariable=var)

    # Number of threads
    num_of_threads_lable = Label(text="Number of threads: ")
    num_of_threads_spin = Spinbox(window, from_=1, to=1000000, width=5)

    # Number of processes
    num_of_processes_lable = Label(text="Number of processes: ")
    n = cpu_count()
    num_of_processes_spin = Spinbox(window, from_=1, to=2*n, width=5)

    btn = Button(window, text="Start Sort", command=startApplication)

    empty_label = Label(text="\n")
    label = Label(text="Run a O(N^2) sort's algorithms\n    in parallel and show graph of times:")

    # List size
    list_size_label2 = Label(text="List size:")
    list_size_spin2 = Spinbox(window, from_=1, to=1000000, width=15, textvariable=var)

    btn2 = Button(window, text="Start", command=showGraph)

    # Thread/Process
    thread_process_label.grid(column=1, row=1)
    thread_rad.grid(column=2, row=1)
    num_of_threads_spin.grid(column=3, row=1)

    process_rad.grid(column=2, row=2)
    num_of_processes_spin.grid(column=3, row=2)

    # Quick/Merge
    quick_merge_lable.grid(column=1, row=3)
    quick_rad.grid(column=2, row=3)
    merge_rad.grid(column=3, row=3)

    # Objects/Integers
    object_integer_label.grid(column=1, row=4)
    object_rad.grid(column=2, row=4)
    integer_rad.grid(column=3, row=4)

    # List size
    list_size_label.grid(column=1, row=5)
    list_size_spin.grid(column=2, row=5)

    # Start Button
    btn.grid(column=2, row=10)

    # Show Button
    empty_label.grid(column=1, row=11)
    label.grid(column=1, row=12)

    # List size
    list_size_label2.grid(column=1, row=13)
    list_size_spin2.grid(column=2, row=13)

    btn2.grid(column=2, row=14)

    window.mainloop()