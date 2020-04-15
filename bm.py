import math
"""
	BM : Boyer Moore Algorithm Module
"""

"""
	@param : pattern,text
	@return : list of index which pattern match the text
"""
def boyer_moore(pattern, text):
	last = last_occurrence_function(pattern, text)
	n = len(text)
	m = len(pattern)
	i = m - 1

	index_list = []
	if (i > n-1):
		return index_list
	j = m-1
	
	while True:
		if pattern[j] == text[i]:
			if j == 0:
				index_list.append(i)
				lo = last.get(text[i])
				i = i + m - min(j, 1 + lo)
				j = m - 1
			else :
				j -= 1
				i -= 1
		else :
			lo = last.get(text[i])
			i = i + m - min(j, 1 + lo)
			j = m - 1

		if i > n - 1 :
			break
	return index_list

"""
	@param : pattern,text
	@return : index of the first pattern occurence in text
"""
def boyer_moore_first_occurence(pattern, text):
	index_list = boyer_moore(pattern,text)
	return index_list[0] if len(index_list) > 0 else None 

"""
	@param : pattern & text
	@return : map of key-value : <character in text> - <its mapping to the pattern>
"""
def last_occurrence_function(pattern, text):
	keys = set(text)
	dict = {}
	for key in keys:
		i = len(pattern)
		while i > 0:
			i -= 1	
			if pattern[i] == key and dict.get(key) is None :
				dict[key] = i
		if dict.get(key) is None:
			dict[key] = -1
	return dict

if __name__ == '__main__':
	text = "abacaabadcabacabaabb"
	pattern = "abacab"

	text1 = "aaaaaaaaa"
	pattern1 = "baaaaa"

	text2 = "a pattern matching algorithm"
	pattern2 = "rithm"

	print(boyer_moore(pattern2,text2))

