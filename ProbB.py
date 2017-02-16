import threading
import os
import math

class thrd(threading.Thread):
    thread_id = 0
    outp = []
    #thread id just for testing purposes, outp is final output
    def __init__(self, filename, start, end):
        threading.Thread.__init__(self)
        self.tid = thrd.thread_id
        thrd.thread_id += 1
        self.fn = filename          #file to be worked on
        self.strt = start           #start of work location in bytes
        self.stop = end             #end of work location in bytes

    def announce(self):
        print 'Thread %d reporting for duty \n' %self.tid
        #more test stuff

    def run():
        self.fn.seek(self.strt)

        #start working slaves.

def linelengths(filenm, ntrh):
    #outp = []
    begin = 0
    #keep track of head of file to be passed to thrd instances

    f = open(filenm)
    fsize = os.path.getsize(f)
    chunks = math.ceil(fsize / ntrh)
    #divvy up the file evenly (approx)

    for i in range(ntrh):
        #start making slave--er i mean threads
        t = thrd(f, begin, i*chunks)
        begin += chunks         #increment before t.run() so no problem (?)
        t.announce()
        t.run()
