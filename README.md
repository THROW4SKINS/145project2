Problem A

The programming in this problem will be fairly straightforward, but it is important that you understand the motivation, as follows.

Imagine a 3-question survey, with each question asking the respondent to rate a product from 1 to 5. There will be 53 = 125 possible patterns, i.e. (1,1,1), (1,1,2),...,(5,5,5). We are interested in determining which patterns in our data set are most common.

For example, say there are 7 people who completed the survey, and they answered (5,4,5), (5,2,3), (5,4,5), (1,4,2), (3,3,3), (5,4,5), (1,4,2). Then the most frequent pattern was (5,4,5), and the second-most frequent one was (1,4,2).

We might store our frequencies in a two-dimensional array, with the first 3 columns being the pattern and the last column being the frequency. So, we'd have 4 rows, one for each of the patterns we found, with one of the rows being (5,4,5,3).

Now consider what would happen if the survey had 50 questions, with a large number of respondents. There would now be 550 possible patterns, and though most patterns would not show up in the data, the above 2-D array would have a ton of rows. That in itself is not so bad, but what if we want to do many queries, asking the frequencies of various patterns? Then we would have to do a search through the array each time, which could be really slow.

A better approach would be the use a Python dictionary. In the above example, we might create a dictionary freqs, with for instance freqs['5,4,5'] equal to 3. This way we could do associative lookups; for instance, we would submit the query '5,4,5' and the return value would be 3. This would be much faster, because Python dictionaries are implemented as hash tables.

The other issue is that real-world data is messy, with a lot of missing values. For example, we might have a record consisting of (5,4,NA), where NA means "not available." This is an R term, roughly the same as Python's None. But it partly matches the (5,4,5) pattern in our data, so we might count it as 2/3 of a match to (5,4,5). So, the frequency of (5,4,5) would be 3 2/3. And if we had had, say, a (5,4,1) record in our data, that would count 2/3 as well. If we have 4 questions in our survey, a record with 2 NAs but which matches an intact record in the other 2 components, it would count as half a match. Partial matches are made only of nonintact patterns to intact patterns.

So here are the specs:

Write a function calcfreqs(infile,nqs,maxrat, with arguments as follows: The input file name is given by infile; the number of questions in the survey is nqs; and the choice of responses is 1...maxrat. The return value is a Python dictionary as described above.
The input file's line format is, e.g.
5 4 NA
Have your code raise an exception, with an error message printed, if the file doesn't exist, or if a line in the file is found to have an error.
Write a function highfreqs(freqs,k), where freqs is the output of calcfreqs(), and k is a positive integer. The return value is the subdictionary corresponding to the patterns with the k highest frequencies. If two different patterns have the same frequency and the latter is among the k highest, include them both. Also, if k is negative, find the least frequent patterns, not the most.
Place your entire code in a file ProblemA.py.
Below is an example, using the file y,

5 4 5
NA 3 3
5 2 3
5 4 5
1 4 2
5 4 NA
4 NA 1
5 4 1
3 3 3
5 2 3
5 4 5
1 4 2
>>> from Freq import *
>>> fr = calcfreqs('y',3,5)
>>> fr
{'5,4,5': 3.6666666666666665, '1,4,2': 2, '5,4,1': 1.6666666666666665,
'3,3,3': 1.6666666666666665, '5,2,3': 2}
>>> highfreqs(fr,2)
{'5,4,5': 3.6666666666666665, '1,4,2': 2, '5,2,3': 2}
Problem B:

Here you will write code to perform a type of file data operation, using Python threads. You are required to use either the thread or threading module.

The problem statement is simple (and the code is not difficult): Write a function with declaration

def linelengths(filenm,ntrh):
which returns a Python list, the ith element of which is the number of characters in line i of the file. Here are the details:

Do not count the EOL character in the line length. But allow for empty lines, i.e. length 0.
If the last byte in the file is not the EOL character, operate as if there is one, i.e. treat the last set of bytes in the file as a line.
Have the threads work on approximately equal chunks of the file, starting at about equally-spaced points. For instance, say the file is 1200 bytes long (including EOLs) and you run 3 threads. Have thread 0 start at byte 0, thread 1 start at byte 400, and thread 2 start at 800.
The point of Problem B is to get experience with interactions between threads. In this case, that will mean having the threads cooperate to create the final list of line lengths. Do not have the parent thread splice together the individual lists found by the child threads.
Hopefully the threaded version is faster than an unthreaded one, due to parallelism. The GIL limits the potential for speed increase, but we may be able to get parallelism via the overlapping of computation and I/O. For Extra Credit, do a timing experiment, probably on a very large file, which you will store in /tmp. Make sure your steps are reproducible by the TA. Please your report in a file Report.txt, a plain ASCII text file.
Put your code in a file ProbB.py.
Test example:

% cat z

1
23
abc
de
f
% od -h z
0000000 310a 320a 0a33 6261 0a63 6564 660a 000a
0000017
wc -c z
15 z
There are 15 bytes in this file, including the EOL character, 0x0a. By the way, note that because this is a Little Endian machine, the order of the reported bytes here is "backwards." For instance, byte 6 has contents, 0x61, byte 7 has contents 0x62.

Say you have 2 threads, so thread 0 works on bytes 0-6 and thread 1 handles 7-14. Thread 0 will find line lengths in its chunk of the file, and thread 1 will work on its chunk.

Note carefully that the 'abc' line is split between the 2 chunks. The threads will have to deal with this, reconciling any discrepancies. Do not have the parent thread do this; it should only set up the threads, call them and then return the list that they cooperatively form.

Calling linelengths('z',2) should return the list [0,1,2,3,2,1].

Problem C:

Here you will write a SimPy simulation program for a very simple model of an online store. Here are the details:

Customer orders arrive at random times, with times between successive orders having a gamma distribution. You call this via random.gammavariate(), with arguments alpha and beta.
The Wikipedia entry for the gamma distribution family has pictures of the density function; their k is Python's alpha and their θ is Python's beta. If you generate, say 1000, random variates using this Python call and draw a histogram, it will look like one of the curves in the picture.

New inventory arrives at random times, independent of whether there are pending customer orders. The distribution of times between deliveries of new inventory will also be modeled as gamma, with different values of alpha and beta than above.
There is only one kind of item sold. Each customer orders a quantity of 1. Each delivery of new stock is a quantity of 1.
Your "main" function will have the declaration
def storesim(maxsimtime,alphac,betac,alphai,betai):
The function returns the following in a tuple:
the mean time it takes for a customer's order to be filled (0 if immediate)
the proportion of customer orders that are filled immediately
the proportion of inventory deliveries that are immediately used to fill a customer order upon arrival of the delivery
Place your code in a file ProbC.py.
Testing:

The call storesim(10000,2,2.2,2,2) should return values of approximately 2.47 and 0.81 for the mean wait and proportion of orders served immediately, respectively.

Note that the mean of a gamma distribution is α β. If the mean time between item deliveries is greater than the mean time between customer order arrivals, the situation is unstable, in that the number of waiting order will go to infinity as time goes to infinity. (This will occur even if the two means are equal.) This may make it difficult to test/debug your code, so I'd advise avoiding this situation.
