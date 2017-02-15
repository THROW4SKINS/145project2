"""
OLD calcfreqs function DOES NOT WORk
    def calcfreqs(infile, nqs, maxrat): 
    freq_dict = {} #Main dictionary to contain all the frequencies 
    f = open(infile, "r") #Open file
    f_list = f.read()
    f_list = f_list.split('\n')
    for x in xrange(0, len(f_list)):
        f_string = ','.join(f_list[x].split(' '))  # Change the format to a 5,5,5,NA
        curr_nqs = len(f_string.split(','))
        if curr_nqs == nqs:
            if not 'NA' in f_string:
                freq_dict.update({f_string: 0})
        else:
            continue
    for x in xrange(0,len(f_list)):
    	f_string = ','.join(f_list[x].split(' ')) #Change the format to a 5,5,5,NA
    	dict_keys = freq_dict.keys()
    	if 'NA' in f_string: #If the line has an NA
    		counter = f_string.count('NA')
    		fixed_f = ''.join(f_string.split('NA'))
    		for y in xrange(0,len(dict_keys)): 
    			if fixed_f in dict_keys[y]:
    				freq_dict[dict_keys[y]] += float(nqs-counter)/nqs
    	elif f_string in dict_keys: #If the line does not have an NA
    		freq_dict[f_string] += 1 
    	else: #If the line does not exist in the dictionary, aka new response
    		freq_dict.update({f_string: 1})
    return freq_dict"""

def calcfreqs(infile, nqs, maxrat):
	global freq_dict    #Our global dictionary to contain all the frequencies
	freq_dict = {}
        f_list = readFile(infile)
	NA_list = []        #We will create an empty list to contain all the NA rows. 
                            #This will make it easier to add nonintact to intact data
	for x in xrange(0, len(f_list)): #Loop through all the elements in the list. Which is the rows of answers
		f_row = f_list[x].split(' ')
		f_string = ','.join(f_row)
		format_check(f_row, nqs, maxrat) #Use the function format_check to test for errors/abnormalities in the file
		if 'NA' in f_row: #Save the NA rows for later
			NA_list.append(f_row)
		elif f_string in freq_dict.keys(): #Add to existing dictionary keys
			freq_dict[f_string] += 1
		else:
			freq_dict.update({f_string: 1}) #Create new keys for non existing dictionary keys
	if NA_list > 0: #Now we go back to the NA rows
		for y in xrange(0,len(NA_list)): 
			in_dict = dict_compare(NA_list[y]) #in_dict contains a list of dictionary elements that the row relates to.
			for z in in_dict:
				counter = NA_list[y].count('NA')
				freq_dict[z] += float(nqs-counter)/nqs #Add in the fraction of the frequency.
	return freq_dict

def readFile(inf):
	f = open(inf, "r") #Open file
	f_list = f.read()
	f_list = f_list.split('\n') #Since the answers are split by a new line, 
                                    #we will use split to change it into a list. 
                                    #Each element in the list is a row of answers, 
                                    #in a string format

	for w in xrange(0,len(f_list)): 
                #Found out my test file have \r cause window is stupid.
                #We will implement this to make sure \r are gone
		f_list[w] = f_list[w].replace('\r', '')

        while f_list[-1] == '':
            del f_list[-1]
            #get rid of any blank rows at the end created by split()

        return f_list


def format_check(inline, nqs, maxrat):
	if len(inline) != nqs: #Check for lengh of answers compared to nqs
		raise Exception('Number of answers in file does not equal to the number of questions in the survey')
	for i in xrange(len(inline)):
		if inline[i] == 'NA':
			continue
		#Need to implement unknown string tester
		elif inline[i].isalpha():
			raise Exception('Unknown string found in file')

                elif inline[i] == '':
                    raise Exception('Empty or missing entry')

		elif int(inline[i]) > maxrat:
			raise Exception('Choice of responses exceeds maxrat')

def dict_compare(inline):
	matches = []
	for a in freq_dict: #Go through all the dictionary keys
		#Here, for each dictionary key, we split it back into a list. 
		#For each element in the list, we make sure that it is the same in the row answers. Such as 5,4,5 and 5,4,NA. We make sure index 0 and 1 are equal
		#For the 'NA', we make it pass so when it compares with any numbers, in this case 5 and NA, it will just ignore the comparison
		#If the index comparison are not the same, break. Otherwise, if we reach the end, then it is the same, and we add that dictionary key to the list of good compares.
		a_sect = a.split(',')
		for b in xrange(len(inline)):
			if a_sect[b] != inline[b]:
				if inline[b] == 'NA':
					pass
				else:
					break
			if b == len(inline)-1:
				matches.append(a)
	return matches

def highfreqs(freqs, k):
    return dict(((d, v) for (d, v) in freqs.iteritems() if v >= k))
