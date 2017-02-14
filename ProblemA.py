def calcfreqs(infile, nqs, maxrat):
    freq_dict = {} #Main dictionary to contain all the frequencies 
    f = open(infile, "r") #Open file
    f_list = f.read()
    f_list = f_list.split('\n')
    for x in xrange(0,len(f_list)):
    	f_string = ','.join(f_list[x].split(' ')) #Change the format to a 5,5,5,NA
    	dict_keys = freq_dict.keys()
    	if 'NA' in f_string: #If the line has an NA
    		counter = f_string.count('NA')
    		fixed_f = ''.join(f_string.split('NA'))
    		for y in xrange(0,len(dict_keys)): 
    			if fixed_f in dict_keys[y]:
    				freq_dict[dict_keys[y]] += float(counter)/nqs
    	elif f_string in dict_keys: #If the line does not have an NA
    		freq_dict[f_string] += 1 
    	else: #If the line does not exist in the dictionary, aka new response
    		freq_dict.update({f_string: 1})


def highfreqs(freqs, k):
    filter(lambda: freqs.values() < k,freqs)
    return freqs

test = calcfreqs('y',3,5)
print(test)
