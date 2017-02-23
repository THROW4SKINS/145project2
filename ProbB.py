import threading
from timeit import default_timer as timer

def linelengths(filenm, ntrh):
    global length_list #Global list to hold our returning list of number of bytes in each line
    #timeTaken = 0
    begin = 0 #Variable to hold which byte for the thread to start
    num_stack = 0 #Number of lines we are currently in
    f = open(filenm,"r") 
    fstring = f.read()
    f_len = len(fstring)
    #Here, we will test if the end of file \n is there or not.
    #For our program, we will proceed as if the \n is not in the string
    #So here, we remove it if it is in the string
    if fstring[-1] == '\n':
        fstring = fstring[:-1]
        fsize = f_len + 1
        length_list = [0] * (fstring.count('\n') + 1)
    else:
        fsize = f_len + 1
        length_list = [0] * (fstring.count('\n') + 1)

    #Algorithm for the chunks of byte each thread will receive.
    #The idea is every thread gets the same number or plus 1
    #With mod, we get the remainder of the division
    #The remainder will be distributed to the first remainder # of threads
    chunk_remain = fsize % ntrh
    chunk_whole = int((fsize - chunk_remain)/ntrh)
    chunk_size = [chunk_whole] * ntrh
    for x in xrange(chunk_remain):
        chunk_size[x] += 1

    #This will hold all our threads
    threads = []
    #tstart = timer()
    #Here we will give each thread their chunk of string to calculate and the line number they're in
    for i in xrange(ntrh):
        f_string = fstring[begin:begin + chunk_size[i]]
        t = threading.Thread(target=string_length,args=(f_string, num_stack))
        threads.append(t)
        begin += chunk_size[i]
        num_stack += f_string.count('\n')
    #Start all the thread
    for thread in threads:
        thread.start()
    #Wait till all the threads are done
    for thread in threads:
        if thread.isAlive():
            thread.join()
    #tend = timer()
    #timeTaken = tend - tstart
    return length_list

def string_length(chunk, num_stack):
    #This function will split the string according to the new line \n.
    #Then add in the number of bytes to the corresponding list index
    line_list = chunk.split('\n')
    for i in range(len(line_list)):
        list_index = num_stack + i
        length_list[list_index] += len(line_list[i])
