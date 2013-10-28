#!/usr/bin/env python
"""
Derek Salama
CS 073
"""
import sys
import codecs
import pdb
from collections import defaultdict
from collections import deque

def parse_grammar_file(filename):
	text = codecs.open(filename, 'r', 'utf8')
	rules = defaultdict(set)
	for line in text:
		words = line.split()

		# skip empty lines
		if len(words) == 0:
				continue

		lhs = words[0]
		rhs = tuple(words[1:-1])
		prob = float(words[-1])
		rules[rhs].add((lhs, prob))
	
	return rules

def productions_for_cells(left, right, rules):
		result = set()
		for t1 in left:
				for t2 in right:
						# pdb.set_trace()
						production = rules[(t1[0], t2[0])]
						if len(production) == 0:
								continue
						for p in production:
							prob = t1[1] * t2[1] * p[1]
							result.add((p[0], prob, t1, t2))
		return result

def pretty_print_matrix(matrix):
		for row in matrix:
				for column in row:
						if len(column) > 0:
								for production in column:
										print production[0] + ": " + str(production[1]),
						else:
								print "\t--\t",
						print "\t",

				print "\n"

def print_cky_parse_tree(root, level):
		for i in range(0, level):
				print "\t",
		print "(",
		print root[0],
		if len(root) == 3: # leef node
			print root[2],
		else:
			print ""
			print_cky_parse_tree(root[2], level + 1)
			print ""
			print_cky_parse_tree(root[3], level + 1)
		print ")",

				

def cky(sentence, rules):
		matrix = [[]]

		# special case for first row
		for w in sentence:
				productions = rules[(w,)]
				cell = tuple(p + (w,) for p in productions)
				matrix[0].append(cell)

		for row in range(1, len(sentence)):
				matrix.append([])
				for column in range(0, len(sentence) - row):
						cell = set()
						cell |= productions_for_cells(matrix[row - 1][column], matrix[0][column + 1], rules)
						cell |= productions_for_cells(matrix[0][column], matrix[row - 1][column + 1], rules)
						matrix[row].append(cell)
		return matrix

if __name__=='__main__':
	grammar_file = sys.argv[1]
	rules = parse_grammar_file(grammar_file)
	sentence_file = sys.argv[2]
	text = codecs.open(sentence_file, 'r', 'utf8')
	for line in text:
			matrix = cky(line.split(), rules)
			pretty_print_matrix(matrix)
			valid_roots = filter(lambda x: x[0] == u"S", matrix[-1][0])
			if len(valid_roots) == 0:
					print "No valid parse for " + line
			else:
					valid_roots.sort(key=lambda x: x[1])
					max_valid_root = valid_roots[-1]
					print_cky_parse_tree(max_valid_root, 0)
					print "\n\n"
