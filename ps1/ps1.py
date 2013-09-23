#!/usr/bin/env python
from __future__ import division
import sys
import codecs
from collections import defaultdict

""" Copied from 'Computation Tips and Tricks' """
""" Modified to ignore punctuation """
def count_words(filename):
    """Read a file and count the frequency of each word"""
    text = codecs.open(filename, 'r', 'utf8')
    countsdict = defaultdict(int)
    punctuation = {".", ",", ":", ";", "!"}

    for line in text:
        words = line.split()
        
        for word in words:
        	if word not in punctuation:
        		countsdict[word.lower()]+=1
            
    return countsdict

if __name__=='__main__':
	input_file = sys.argv[1]
	countsdict = count_words(input_file)

	tokens = 0
	for count in countsdict.values():
		tokens += count
	word_types = len(countsdict.keys())

	print "Tokens: " + str(tokens)
	print "Types: " + str(word_types)
	print "Token-to-Type ration: " + str(tokens / word_types)

