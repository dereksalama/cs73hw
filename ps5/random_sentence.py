#!/usr/bin/env python
"""
Derek Salama
CS 073
"""
import sys
import codecs
import random
import pdb
from collections import defaultdict

comment = "#"

def parse_input_file(filename):
	text = codecs.open(filename, 'r', 'utf8')
	rules = defaultdict(set)
	for line in text:
		if line[0] == comment:
			continue
		words = line.split()
		if len(words) == 0:
				continue

		lhs = words[0]
		rhs = tuple(words[1:])
		rules[lhs].add(rhs)
	
	return rules

def expand(term, rules):
	#pdb.set_trace()
	productions = rules[term]
	if len(productions) == 0: #terminal
		print term,
		return
	rhs = random.sample(productions, 1)[0]
	for t in rhs:
		expand(t, rules)

if __name__=='__main__':
	input_file = sys.argv[1]
	rules = parse_input_file(input_file)
	expand("ROOT", rules)
