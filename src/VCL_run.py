import glob
import os
from re import A
import time
#import matplotlib.pyplot as plt
from array import array
from datetime import date, datetime


class TimSort:
    MIN_MERGE = 64

    def __init__(self):
        '''the datastructures required'''
        self.array = []

    def readFile(self, dataset, log_file_name):
        '''read file x.log'''

        path = dataset + '/' + log_file_name
        log_file = open(path, 'r', encoding='ISO-8859-15')
        Lines = log_file.readlines()
        for line in Lines:
            line = line.strip()
            lst = line.split(" ", 1)
            try:
                # lst[0] = datetime.fromisoformat(lst[0])
                lst[0] = int(datetime.fromisoformat(lst[0]).strftime("%Y%m%d%H%M%S"))
            except:
                continue
            self.array.append(lst)

    def writeFile(self, out_file_name):
        '''write to a file'''
        self.array = ["{0} {1}\n".format(x1, x2) for (x1, x2) in self.array]
        with open(out_file_name, 'w') as out_file:
            out_file.writelines(self.array)

    def printArray(self):
        '''print the array'''
        print(self.array)

    def calcMinRun(self, n):
        '''calculation of minimum run value'''
        r = 0
        while n >= self.MIN_MERGE:
            r |= n & 1
            n >>= 1
        return (n + r)

    def insertionSort(self, left, right):
        '''performing insertion sort'''
        for i in range(left + 1, right + 1):
            j = i
            while j > left and self.array[j][0] < self.array[j - 1][0]:
                self.array[j], self.array[j - 1] = self.array[j - 1], self.array[j]
                j -= 1

    def merge(self, l, m, r):
        '''performing merge operation'''
        len1, len2 = m - l + 1, r - m
        left, right = [], []
        for i in range(0, len1):
            left.append(self.array[l + i])
        for i in range(0, len2):
            right.append(self.array[m + 1 + i])

        i, j, k = 0, 0, l

        while i < len1 and j < len2:
            if left[i][0] <= right[j][0]:
                self.array[k] = left[i]
                i += 1
            else:
                self.array[k] = right[j]
                j += 1

            k += 1

        while i < len1:
            self.array[k] = left[i]
            k += 1
            i += 1

        while j < len2:
            self.array[k] = right[j]
            k += 1
            j += 1

    def timSort(self):
        '''main Tim Sort function'''
        n = len(self.array)
        minRun = self.calcMinRun(n)

        for start in range(0, n, minRun):
            end = min(start + minRun - 1, n - 1)
            self.insertionSort(start, end)

        size = minRun
        while size < n:

            for left in range(0, n, 2 * size):
                mid = min(n - 1, left + size - 1)
                right = min((left + 2 * size - 1), (n - 1))

                if mid < right:
                    self.merge(left, mid, right)

            size = 2 * size

    def insertSort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key

    def isSorted(self):
        '''check if the array is sorted'''
        n = len(self.array)
        if n == 0 or n == 1:
            return True

        for i in range(1, n):
            if self.array[i - 1][0] > self.array[i][0]:
                return False
        return True
    
    def mergeSort(self, arr):
        '''merge sort function'''
        if len(arr) > 1:
            mid = len(arr)//2
            L = arr[:mid]
            R = arr[mid:]
            
            self.mergeSort(L)
  
            self.mergeSort(R)
  
            i = j = k = 0
  
            while i < len(L) and j < len(R):
                if L[i][0] < R[j][0]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
  
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
  
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
    
    def main(self, dataset, algorithm):
        self.elapsed_time = []
        self.file_name = []
        entries = os.listdir(dataset.upper() + '/')
        self.new_file_name = []
        print(entries)

        for entry in entries:
            if entry != '.DS_Store':
                file_size = entry.split('.')
                file_size_number = int(file_size[0])
                self.new_file_name.append(file_size_number)
        self.new_file_name = sorted(self.new_file_name)
        count = 0
        count_limit = 0
        if algorithm.lower().__contains__("tim") or algorithm.lower().__contains__("merge"):
            count_limit = 23
        else:
            count_limit = 20 
        for name in self.new_file_name:
            if count < count_limit:
                name = str(name) + '.log'
                self.readFile(dataset.upper(), name)  # change file name here!
                # self.printArray()
                file = name.split('.')
                line_number = file[0]
                self.file_name.append(line_number)
                t = time.process_time()
                if algorithm.lower().__contains__("insertion"):
                    self.insertSort()
                elif algorithm.lower().__contains__("tim"):
                    self.timSort();
                else:
                    self.mergeSort(self.array)
                time_taken = time.process_time() - t
                print(time_taken)
                self.elapsed_time.append(time_taken)
                print("Sorting complete.")
                # self.printArray()
                print("Array Sorted? ", self.isSorted())
                print('Now writing.')
                self.writeFile('sorted_' + name)  # change file name here!
                self.array = []
                count = count + 1
        # self.timSort()
        # print(elapsed_time)
        #plt.plot(self.elapsed_time, self.file_name, '-ok')
        #plt.xlabel('Time')
        # naming the y axis
        #plt.ylabel('Lines')
        # giving a title to my graph
        #plt.title('Plot')
        # function to show the plot
        #plt.show()


if __name__ == '__main__':
    dataset_you_want_to_run_against = input("Enter the dataset you want to run against: ")
    sort_algorithm = input("Enter the sort algorithm you want to use: ")
    obj = TimSort() # calling the class
    obj.main(dataset_you_want_to_run_against, sort_algorithm)