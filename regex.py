"""
	Regex : Regular Expression Algorithm Module
"""
import re  	# Regular expression module in python

def regex_function(pattern, text):
	iter = re.finditer(pattern, text)
	return [m.start(0) for m in iter]

if __name__ == '__main__' :
	text = "abacaabadcabacabaabb"
	pattern = "abacab"

	text1 = "aaaaaaaaa"
	pattern1 = "baaaaa"

	text2 = "a pattern matching algorithm"
	pattern2 = "rithm"

	print(regex_function(pattern, text))
	print(regex_function(pattern1,text1))
	print(regex_function(pattern2,text2))