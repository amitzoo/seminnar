import threading
import random
import time
import plotly.express as px
import pandas as pd


class sort:

    def __init__(self, list_size):
        self.start_insertion_sort = 0
        self.start_bubblesort = 0
        self.start_selection_sort = 0
        self.end_insertion_sort = 0
        self.end_selection_sort = 0
        self.end_bubblesort = 0
        self.list_size = list_size

    def insertion_sort(self, InputList):
        self.start_insertion_sort = time.perf_counter()

        for i in range(1, len(InputList)):
            j = i-1
            nxt_element = InputList[i]

            while (InputList[j] > nxt_element) and (j >= 0):
                InputList[j+1] = InputList[j]
                j=j-1
            InputList[j+1] = nxt_element

        self.end_insertion_sort = time.perf_counter()

    def bubblesort(self, list):
        self.start_bubblesort = time.perf_counter()

        for iter_num in range(len(list)-1,0,-1):
            for idx in range(iter_num):
                if list[idx]>list[idx+1]:
                    temp = list[idx]
                    list[idx] = list[idx+1]
                    list[idx+1] = temp

        self.end_bubblesort = time.perf_counter()

    def selection_sort(self, input_list):
        self.start_selection_sort = time.perf_counter()

        for idx in range(len(input_list)):
            min_idx = idx

            for j in range( idx +1, len(input_list)):
                if input_list[min_idx] > input_list[j]:
                    min_idx = j

            input_list[idx], input_list[min_idx] = input_list[min_idx], input_list[idx]

        self.end_selection_sort = time.perf_counter()

    def createGraph(self):

        lyst1 = random.sample(range(self.list_size*2), self.list_size)
        lyst2 = []
        lyst3 = []

        for a in range(len(lyst1)):
            lyst2.append(lyst1[a])
            lyst3.append(lyst1[a])

        x_vals = ['Insertion Sort', 'Bubble Sort', 'Selection Sort']
        y_vals = []

        print("wait for a while ... ")

        p1 = threading.Thread(target=self.insertion_sort, args=[lyst1])
        p2 = threading.Thread(target=self.bubblesort, args=[lyst2])
        p3 = threading.Thread(target=self.selection_sort, args=[lyst3])

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()


        y_vals.append(self.end_insertion_sort - self.start_insertion_sort)
        y_vals.append(self.end_bubblesort - self.start_bubblesort)
        y_vals.append(self.end_selection_sort - self.start_selection_sort)

        #print("\ninsertion_sort:\n", lyst1, "\nbubblesort:\n", lyst2, "\nselection_sort:\n", lyst3)

        y_vals_1 = [[],[],[]]
        mx = int(max(y_vals)+1)

        for a in range(mx*2):
            if (y_vals[0] <= (a/2)):
                y_vals_1[0].append(y_vals[0])
            else:
                y_vals_1[0].append(a/2)

            if (y_vals[1] <= (a/2)):
                y_vals_1[1].append(y_vals[1])
            else:
                y_vals_1[1].append(a/2)

            if (y_vals[2] <= (a/2)):
                y_vals_1[2].append(y_vals[2])
            else:
                y_vals_1[2].append(a/2)

        tmp = [[],[],[]]
        for a in range(len(y_vals_1[0])):
            tmp[0].append('Insertion Sort')
            tmp[1].append(y_vals_1[0][a])
            tmp[2].append(a/2)

            tmp[0].append('Bubble Sort')
            tmp[1].append(y_vals_1[1][a])
            tmp[2].append(a/2)

            tmp[0].append('Selection Sort')
            tmp[1].append(y_vals_1[2][a])
            tmp[2].append(a/2)

        df = pd.DataFrame()
        df['Algos'] = tmp[0]
        df['Time(s)'] = tmp[1]
        df['Time'] = tmp[2]


        fig = px.bar(df, x="Algos", y="Time(s)", color="Algos", animation_frame="Time", animation_group="Time(s)", range_y=[0,mx])
        fig.show()
