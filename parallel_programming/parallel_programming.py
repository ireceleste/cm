#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 08:40:13 2022

@author: IreneCelestino
"""

# =============================================================================
# ESEMPI : parallel programming - threads e processi
# =============================================================================


"""


from multiprocessing import Process
import time
import os


def f(name):
    print('Hello '+name)
    time.sleep(1)  # aspetta 1s prima di uscire


def f0(name):
    print()
    print( "-----> function " +name)
    print ( "I am still the main process with ID "
    +str(os.getpid())+ " my father is ID:" +str(os.getppid()))
    
def f1(name):
    print()
    print( "-----> function " +name)    
    print ( "I am the first sub-process with ID "
    +str(os.getpid())+ " my father is ID:" +str(os.getppid()))
    f2('two')

def f2(name):
    print()
    print( "-----> function " +name)
    print ( "I am still the first sub-process with ID "
    +str(os.getpid())+ " my father is ID:" +str(os.getppid()))
    print("This is the end!")



# MAIN
if __name__== "__main__":
    p = Process(target=f, args=('World',))
    p.start()
    print("ciao1")
    p.join()  # aspettare che p sia finito prima di andare avanti
    print("ciao2")

    print('\n')
    time.sleep(1)

    print ( "I am the main process with ID: " +str(os.getpid())
           + " my father is ID:" +str(os.getppid()))
    f0('zero')
    p1 = Process(target=f1, args=("one" ,))
    p1.start()
    p1.join()
"""

# =============================================================================
# FourProcesses.py
# =============================================================================

"""
import multiprocessing as mp

# define a example function

def Hello(pos,name, output):
    msg = "Hello "+name
    output.put((pos, msg))  # mette output in queue

if __name__=="__main__":
    # Define an output queue
    output = mp.Queue()
    
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=Hello, args=(x, "Gianluca", output)) for x in range(4)]
    # Run processes: lanciati in parallelo
    for p in processes:
        p.start()
    # Exit the completed processes
    for p in processes:
        p.join()
    # Get process results from the output queue
    results = [output.get() for p in processes]
    print(results) 
"""

# =============================================================================
# Pool Map: definiamo un insieme di posti in cui si fanno i processi (pool)
# La coda viene fatta automaticamente con pool.map
# =============================================================================

"""
import multiprocessing as mp
import os
import time


def cube(x):
    print("ID: " + str(os.getpid())+" Father: "+str(os.getppid()))
    time.sleep(1)
    return x**3

#MAIN
if __name__=="__main__":
    start=time.time()
    pool = mp.Pool(processes=4)
    results = pool.map_async(cube,range(1,7))
    end=time.time()
    print("\n elapsed time after starting = " + str(end-start))
    
    print(results.get())
    end=time.time()
    print("\n elapsed time after executing= " + str(end-start))
    
"""

# =============================================================================
# Communication between processes - modo sbagliato: non posso usare variabile 
# globale per mettere insieme risultati di processi diversi: ogni processo 
# usa zona di memoria diversa: result ha un indirizzo diverso in  processo 
# rispetto al main
# =============================================================================

"""
import multiprocessing
# empty list with global scope
result = []
def square_list(mylist):
    global result
    for num in mylist:
        result.append(num * num)
        print("Result(in process p1):"+str(result))

#MAIN
if __name__=="__main__":
    # input list
    mylist = [1,2,3,4]
    # creating new process
    p1 = multiprocessing.Process(target=square_list,args=(mylist,))
    # starting process
    p1.start()
    # wait until process is finished
    p1.join()
    # print global result list
    print("Result(in main program): "+str(result))
"""

# =============================================================================
# Communication with shared memory
# =============================================================================

"""
import multiprocessing

def square_list(mylist, result, square_sum):
    for idx, num in enumerate(mylist):
        result[idx] = num * num
    # square_sum value
    square_sum.value = sum(result)
    # print result Array
    print("Result (in process p1): " +str(result[:]))
    # print square_sum Value
    print("Sum of squares (in process p1): " +str(square_sum.value))

if __name__=="__main__":
    # input list
    mylist = [1,2,3,4]
    # creating Array of int data type with space for 4 integers
    result = multiprocessing.Array('i', 4)
    # creating Value of int data type
    square_sum = multiprocessing.Value('i')
    # creating new process
    p1 = multiprocessing.Process(target=square_list, args=(mylist, result, square_sum))
    # starting process
    p1.start()
    # wait until process is finished
    p1.join()
    # print result array
    print("Result(in main program): " +str(result[:]))
    # print square_sum Value
    print("Sum of squares(in main program): " +str(square_sum.value))
    
"""

# =============================================================================
# SYNChro: modo sbagliato -> se si fanno partire contemporaneamente due 
# processi che scrivono su stessa parte di memoria, a volte vince uno e a 
# volte l'altro e risultato ogni volta diverso --> serve usare mutex/semafori
# =============================================================================

"""
import multiprocessing

def withdraw(balance):
    for x in range(10000):
        balance.value = balance.value - 1

def deposit(balance):
    for x in range(10000):
        balance.value = balance.value + 1

def perform_transactions():
    # initial balance (in shared memory)
    balance = multiprocessing.Value('i', 100)
    # creating new processes
    p1 = multiprocessing.Process(target=withdraw, args=(balance,))
    p2 = multiprocessing.Process(target=deposit, args=(balance,))
    # starting processes
    p1.start()
    p2.start()
    # wait until processes are finished
    p1.join()
    p2.join()
    # print final balance
    print("Final balance = {}".format(balance.value))
#MAIN
if __name__=="__main__":
    for x in range(10):
    # perform same transaction process 10 times
        perform_transactions()
"""


"""
import multiprocessing
# function to withdraw from account
def withdraw(balance, lock):
    for x in range(10000):
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()
# function to deposit to account
def deposit(balance, lock):
    for x in range(10000):
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()
def perform_transactions():
    # initial balance (in shared memory)
    balance = multiprocessing.Value('i', 100)
    # creating a lock object
    lock = multiprocessing.Lock()
    # creating new processes
    p1 = multiprocessing.Process(target=withdraw, args=(balance,lock))
    p2 = multiprocessing.Process(target=deposit, args=(balance,lock))
    # starting processes
    p1.start()
    p2.start()
    # wait until processes are finished
    p1.join()
    p2.join()
    # print final balance
    print("Final balance = "+str(balance.value))

#MAIN
for x in range(10):
# perform same transaction process 10 times
    perform_transactions() 
    
"""

# =============================================================================
# Threads
# =============================================================================
"""
import threading
import os
def task1():
    print("Task 1 assigned to thread: "+threading.current_thread().name)
    print("ID of process running task 1: "+str(os.getpid()))

def task2():
    print("Task 2 assigned to thread: "+threading.current_thread().name)
    print("ID of process running task 2: "+str(os.getpid()))
#MAIN
if __name__=="__main__":
# print ID of current process
    print("ID of process running main program: "+str(os.getpid()))
    # print name of main thread
    print("Main thread name: "+threading.main_thread().name)
    # creating threads
    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2')
    # starting threads
    t1.start()
    t2.start()
    # wait until all threads finish
    t1.join()
    t2.join()
    
    
    
"""
import requests
import threading as thr
from time import perf_counter

buffer_size=1024
#define a function to manage the download
def download(url):
    response = requests.get(url, stream=True)
    filename = url.split("/")[-1]
    with open(filename,"wb") as f:
        for data in response.iter_content(buffer_size):
                f.write(data)
#MAIN
if __name__ == "__main__":
    urls= [
    "http://cds.cern.ch/record/2690508/files/201909-262_01.jpg",
    "http://cds.cern.ch/record/2274473/files/05-07-2017_Calorimeters.jpg",
    "http://cds.cern.ch/record/2274473/files/08-07-2017_Spectrometer_magnet.jpg",
    "http://cds.cern.ch/record/2127067/files/_MG_3944.jpg",
    "http://cds.cern.ch/record/2274473/files/08-07-2017_Electronics.jpg",
    ]
    t = perf_counter()
    #sequential download
    for url in urls:
        download(url)
    print("Time serial: "+str(perf_counter()-t) +" s")
    
    #define 5 threads
    threads = [thr.Thread(target=download, args=(urls[x],)) for x in range(4)]
    t = perf_counter()
    #start threads
    for thread in threads:
        thread.start()
    #join threads
    for thread in threads:
        thread.join()
    print("Time con 5 threads: "+str(perf_counter()-t))