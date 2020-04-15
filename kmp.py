"""
	KMP : Knuth-Morris-Pratt Algorithm Module
"""

"""
	@param : pattern,text
	@return : list of index which pattern match the text
"""
def knuth_morris_prath(pattern, text) :
	n = len(text)						# Text length cache
	m = len(pattern)					# Pattern length cache
	i = 0								# Text traverse pointer tracker
	j = 0								# Pattern traverse pointer tracker			
	fail = failure_function(pattern)	# Border function cache
	index_arr = []						# holder for all pattern occurence in text

	while(i < n) :
		if (pattern[j] == text[i]):
			if (j == m - 1) :
				index_arr.append(i - m + 1)
			i+=1
			j+=1
		elif j > 0:
			j = fail[j-1]
		else :
			i+=1
	return index_arr

"""
	@param : pattern,text
	@return : index of the first pattern occurence in text
"""
def kmp_first_occurence(pattern,text):
	index_list = knuth_morris_prath(pattern,text)
	return index_list[0] if len(index_list) > 0 else None 


"""
	@param : pattern
	@return : list of border / failure value for KMP algorithm preprocessing
"""
def failure_function(pattern):
	fail = [0] * len(pattern)
	fail[0] = 0

	m = len(pattern)
	j = 0
	i = 1

	while(i < m):
		if pattern[j] == pattern[i]:
			fail[i] = j+1
			i+=1
			j+=1
		elif j > 0:
			j = fail[j-1]

		else :
			fail[i] = 0
			i+=1

	return fail

"""
	Tester program
"""
if __name__ == '__main__':
	text = "abacaabac cabacabaabb"
	pattern = "uuuuuuu"

	print("Border Function : ", border_function(pattern))

	print(f"Text: {text}")
	print(f"Pattern : {pattern}")

	print(f"First index occurece : {knuth_morris_prath(pattern,text)}")
	
