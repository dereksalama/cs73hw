#!/usr/bin/env python
"""
Problem Set 1
Derek Salama
CS 073
9/27/13

To execute my program, please run python ps2.py [path_to_text].
I have encluded the text files in my submission, so you can run it
from this directory with:
	python ps2.py text/*

Please note that all of my output is in log_2.

"""
from __future__ import division
import codecs
import sys	
import string
from collections import defaultdict
from math import log

hamilton_training_files = set( str(x) + ".txt" for x in (1, 6, 7, 8, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29))
hamilton_test_files = set( str(x) + ".txt" for x in (9, 11, 12))
madison_training_files = set( str(x) + ".txt" for x in (15, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46))
madison_test_files = set( str(x) + ".txt" for x in (47, 48, 58))
unknown_files = set (str(x) + ".txt" for x in (49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63))

madison_unigram_model = {}
hamilton_unigram_model = {}

def tokenize(lines):
	result = []
	remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

	for line in lines:
		#remove punctuation
		s = line.translate(remove_punctuation_map).lower()

		words = s.split()
		result.extend(words)

	return result

def add_counts(countsdict, tokens):
	for w in tokens:
		countsdict[w] += 1

""" Found recipe for creating pairs on Stackoverflow """
""" http://stackoverflow.com/questions/1257413/iterate-over-pairs-in-a-list-circular-fashion-in-python/1257446#1257446 """
def pair_iter(lst):
	i = iter(lst)
	prev = i.next()
	yield None, prev # First word is unigram
	for item in i:
		yield prev, item
		prev = item

def unigram_relative_freq(countsdict):
	countsdict["<UNK>"] = 1
	total_tokens = sum(countsdict.values())
	return {w: c / total_tokens for (w, c) in countsdict.items()}

def bigram_relative_freq(countsdict):
	# No UNK
	total_tokens = sum(countsdict.values())
	return {w: c / total_tokens for (w, c) in countsdict.items()}

def unigram_log_p(w, P):
	return sum(map(lambda w_i: unigram_log_freq(w_i, P), w))

def unigram_log_ppl(w, P):
	p_w = unigram_log_p(w, P)
	return -p_w / len(w)

def unigram_freq(w_i, P):
	if (w_i in P):
		return P[w_i]
	else:
		return P["<UNK>"]

def unigram_log_freq(w_i, P):
	return log(unigram_freq(w_i, P), 2)

def bigram_log_ppl(w, P_bi, P_uni, gamma):
	p_w = sum(map(lambda w_i: bigram_log_freq(w_i, P_bi, P_uni, gamma), w))
	return -p_w / len(w)

def bigram_log_freq(w_i, P_bi, P_uni, gamma):
	# Special case for first word
	if (w_i[0] == None):
		return unigram_log_freq(w_i[1], P_uni)

	bigram = P_bi.get(w_i, 0) * (1 - gamma)
	unigram = unigram_freq(w_i[1], P_uni) * gamma
	return log(bigram + unigram, 2)

def unigram_models_with_prior(filepath_dict, hamilton_files, madison_files, test_files, p_hamilton, p_madison):
	global hamilton_unigram_model
	global madison_unigram_model

	hamilton_uni_count = defaultdict(int)
	for filename in hamilton_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		text.next() # advance past author
		add_counts(hamilton_uni_count, tokenize(text))
	hamilton_unigram_model = unigram_relative_freq(hamilton_uni_count)

	madison_uni_count = defaultdict(int)
	for filename in madison_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		text.next() # advance past author
		add_counts(madison_uni_count, tokenize(text))
	madison_unigram_model = unigram_relative_freq(madison_uni_count)

	print string.rjust("File", 5), 
	print string.rjust("Hamilton", 15), string.rjust("Madison", 15),
	print string.rjust("Guess", 10), string.rjust("Actual", 10)
	print "------------------------------------------------------------"
	for filename in test_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		author = text.next() # advance past author
		words = tokenize(text)
		ham_p = unigram_log_p(words, hamilton_unigram_model) + log(p_hamilton, 2)
		mad_p = unigram_log_p(words, madison_unigram_model) + log(p_madison, 2)
		print filename.rjust(7, " "),
		print str(ham_p).rjust(15), str(mad_p).rjust(15),
		if (ham_p > mad_p):
			print string.rjust("Hamilton", 10),
		else:
			print string.rjust("Madison", 10),
		print author.rjust(10)

def unigram_models(filepath_dict, hamilton_files, madison_files, test_files):
	global hamilton_unigram_model
	global madison_unigram_model

	hamilton_uni_count = defaultdict(int)
	for filename in hamilton_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		text.next() # advance past author
		add_counts(hamilton_uni_count, tokenize(text))
	hamilton_unigram_model = unigram_relative_freq(hamilton_uni_count)

	madison_uni_count = defaultdict(int)
	for filename in madison_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		text.next() # advance past author
		add_counts(madison_uni_count, tokenize(text))
	madison_unigram_model = unigram_relative_freq(madison_uni_count)

	print string.rjust("File", 5), 
	print string.rjust("Hamilton", 15), string.rjust("Madison", 15),
	print string.rjust("Guess", 10), string.rjust("Actual", 10)
	print "------------------------------------------------------------"
	for filename in test_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		author = text.next() # advance past author
		words = tokenize(text)
		ham_ppl = unigram_log_ppl(words, hamilton_unigram_model)
		mad_ppl = unigram_log_ppl(words, madison_unigram_model)
		print filename.rjust(7, " "),
		print str(ham_ppl).rjust(15), str(mad_ppl).rjust(15),
		if (ham_ppl < mad_ppl):
			print string.rjust("Hamilton", 10),
		else:
			print string.rjust("Madison", 10),
		print author.rjust(10)

def bigram_models(filepath_dict, gamma, hamilton_files, madison_files, test_files):
	global hamilton_unigram_model
	global madison_unigram_model

	hamilton_count = defaultdict(int)
	for filename in hamilton_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		text.next() # advance past author
		bigrams = [pair_iter(tokenize(text))][1:]
		add_counts(hamilton_count, bigrams)
	hamilton_bigram_model = bigram_relative_freq(hamilton_count)

	madison_count = defaultdict(int)
	for filename in madison_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		text.next() # advance past author
		bigrams = [pair_iter(tokenize(text))][1:]
		add_counts(madison_count, bigrams)
	madison_bigram_model = bigram_relative_freq(madison_count)

	print string.rjust("File", 5), 
	print string.rjust("Hamilton", 15), string.rjust("Madison", 15),
	print string.rjust("Guess", 10), string.rjust("Actual", 10)
	print "------------------------------------------------------------"
	for filename in test_files:
		text = codecs.open(filepath_dict[filename], 'r', 'utf8')
		author = text.next() # advance past author
		bigrams = list(pair_iter(tokenize(text)))
		ham_ppl = bigram_log_ppl(bigrams, hamilton_bigram_model, hamilton_unigram_model, gamma)
		mad_ppl = bigram_log_ppl(bigrams, madison_bigram_model, madison_unigram_model, gamma)
		print filename.rjust(7, " "),
		print str(ham_ppl).rjust(15), str(mad_ppl).rjust(15),
		if (ham_ppl < mad_ppl):
			print string.rjust("Hamilton", 10),
		else:
			print string.rjust("Madison", 10),
		print author.rjust(10)

if __name__=='__main__':
	filepath_dict = {}
	for filepath in sys.argv[1:]:
		filename = filepath.split("/")[-1]
		filepath_dict[filename] = filepath
	#t1 =  text = codecs.open("text/1.txt", 'r', 'utf8')
	#t1.next()
	#print(tokenize(t1))
	print "========UNIGRAM (log(Perplexity))========"
	unigram_models(filepath_dict, hamilton_training_files, madison_training_files, hamilton_test_files | madison_test_files)
	print "========BIGRAM (log(Perplexity))========"
	bigram_models(filepath_dict, .2, hamilton_training_files, madison_training_files, hamilton_test_files | madison_test_files)
	print "========IDENTIFICATION WITHOUT PRIOR (log(Perplexity))========"
	unigram_models(filepath_dict, hamilton_training_files | hamilton_test_files, madison_training_files | madison_test_files, unknown_files)
	print "========IDENTIFICATION WITH PRIOR (Unigram, log(P(w|author)P(author))========"
	unigram_models_with_prior(filepath_dict, hamilton_training_files | hamilton_test_files, madison_training_files | madison_test_files, unknown_files, 0.78, 0.22)


