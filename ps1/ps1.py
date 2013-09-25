#!/usr/bin/env python
"""
Problem Set 1
Derek Salama
CS 073
9/27/13
"""

from __future__ import division
import sys
import codecs
from collections import defaultdict
from math import log
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

""" Copied from 'Computation Tips and Tricks' """
""" Modified to ignore punctuation """
def count_words(filename):
    """Read a file and count the frequency of each word"""
    text = codecs.open(filename, 'r', 'utf8')
    countsdict = defaultdict(int)
    punctuation = {".", ",", ":", ";", "!", "-"}

    for line in text:
        words = line.split()
        
        for word in words:
        	if word not in punctuation:
        		countsdict[word.lower()]+=1
            
    return countsdict

def plot_type_length_freq(words):
	lengths = defaultdict(int)
	# Count number of types for each length
	for w in words:
		lengths[len(w)] += 1

	lengths_dist = []
	max_length = max(lengths.values())

	# Find Y value for x in range (0, max)
	for i in range(max_length):
		lengths_dist.append(lengths[i] / len(words))

	plt.bar(range(max_length), lengths_dist)
	plt.ylabel("Frequency")
	plt.xlabel("Word Type Length")
	plt.title("Word Type Length Distribution")

	plt.show()

def plot_token_length_freq(countsdict):
	lengths = defaultdict(int)
	total_words = sum(countsdict.values())
	# Count number of tokens for each length
	for (w, count) in countsdict.items():
		lengths[len(w)] += count

	lengths_dist = []
	max_length = max(lengths.values())

	# Calculate Y value for each x
	for i in range(max_length):
		lengths_dist.append(lengths[i] / total_words)

	plt.bar(range(max_length), lengths_dist)
	plt.ylabel("Frequency")
	plt.xlabel("Word Token Length")
	plt.title("Word Token Length Distribution")

	plt.show()

def plot_rank_vs_freq(frequencies):
	frequencies.sort(reverse=True)

	# find corresponding rank by enumerating frequencies, starting at 1
	ranks = [i for i,f in enumerate(frequencies, start=1)]

	plt.loglog(ranks, frequencies, basex=2, basey=2)
	plt.ylabel("Frequency")
	plt.xlabel("Rank")
	plt.title("Frequency vs. Rank")

	plt.show()

if __name__=='__main__':
	input_file = sys.argv[1]
	countsdict = count_words(input_file)

	tokens = sum(countsdict.values())
	word_types = len(countsdict.keys())

	print "Tokens: " + str(tokens)
	print "Types: " + str(word_types)
	print "Token-to-Type ration: " + str(tokens / word_types)

	# divide each token count by total tokens to get frequencies
	rel_frequencies = map(lambda x: x / tokens, countsdict.values())
	entropy = sum(map(lambda x: -1 * x * log(x, 2), rel_frequencies))
	print "Entropy: " + str(entropy) + " bits"

	# Please note that you must close each plot before the next one will show
	plot_token_length_freq(countsdict)
	plot_type_length_freq(countsdict.keys())
	plot_rank_vs_freq(countsdict.values())

