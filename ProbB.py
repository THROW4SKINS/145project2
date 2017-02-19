import threading
import math

def linelengths(filenm, ntrh):
    global length_list
    length_list = []
    begin = 0
    f = open(filenm,"r")
    fstring = f.read()
    if fstring[-1] == '\n':
        fsize = len(fstring)
    else:
        fsize = len(fstring) + 1
    chunk_size = math.ceil(fsize / ntrh)
    chunk_size = int(chunk_size)
    threads = []

    for i in range(ntrh):
        t = threading.Thread(target=string_length,args=(fstring, begin, chunk_size))
        t.start()
        threads.append(t)
        begin += chunk_size
    for thread in threads:
        thread.join()
    print("===============" )
    print(length_list)
    return length_list

def string_length(f_string, begin, chunk_size):
    cur_length_list = []
    chunk = f_string[begin:begin + chunk_size]
    line_list = chunk.split('\n')
    for i in range(len(line_list)):
        size = len(line_list[i])
        cur_length_list.append(size)
    print(cur_length_list)
    for j in range(len(cur_length_list)):
        if len(length_list) != 0 and j == 0:
            length_list[-1] += cur_length_list[0]
        else:
            length_list.append(cur_length_list[j])

test = linelengths('z',2)
print(test)
