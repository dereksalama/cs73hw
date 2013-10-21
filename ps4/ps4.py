# Derek Salama
# CS 73
# Assignment 4
# Please note that substantial portions of this code
# came from my assignment 3 submission

from __future__ import division
import codecs
import sys
import pdb

from random import random
from math import log
from collections import defaultdict

def log2(n):
	if n == 0:
		return 0
	else:
		return log(n, 2)

# scale all probabilities to prevent underflow
forward_const = 1e5

convergence_threshold = 10 ** -4

def forward(emissions, transitions, sequence):
	unique_states = set(key[0] for key in emissions.keys())
	matrix = defaultdict(list)

	# Initialize: fill out first column
	for state in unique_states:
		p_transition = transitions[(u'#', state)]
		p_emission = emissions[(state, sequence[0])]
		matrix[state].append(forward_const * p_transition * p_emission)

	# General Case
	# Loop through observation
	for (i, c) in enumerate(sequence[1:], start=1):
		# loop through each state for given observation
		for current_state in unique_states:
			p_emission = emissions[(current_state, c)]
			total_prob = 0
			# Inner loop: all possible previous states
			for previous_state in unique_states:
				p_transition = transitions[(previous_state, current_state)]
				p_previous_state = matrix[previous_state][i-1]
				total_prob += forward_const * p_previous_state * p_emission * p_transition
			matrix[current_state].append(total_prob)

	for l in matrix.values():
		for i in range(len(sequence)):
			l[i] = log2(l[i]) - (log2(forward_const) * (i + 1))

	return matrix

def forward_total(matrix):
	return log2(sum(2 ** l[-1] for l in matrix.values()))


def backward(emissions, transitions, sequence):
	unique_states = set(key[0] for key in emissions.keys())
	matrix = defaultdict(list)

	# Initialize: fill out last column
	for state in unique_states:
		matrix[state].append(1)

	rev = sequence[::-1]
	for i in range(1, len(rev)):
		for current_state in unique_states:
			total_prob = 0
			for next_state in unique_states:
				p_emission = emissions[(next_state, rev[i - 1])]
				p_transition = transitions[(current_state, next_state)]
				p_next_state = matrix[next_state][i - 1]
				total_prob += forward_const * p_emission * p_transition * p_next_state
			matrix[current_state].append(total_prob)

	for l in matrix.values():
		for i in range(len(l)):
			l[i] = log2(l[i]) - (log2(forward_const) * i)
		l.reverse()

	return matrix

def backward_total(emissions, transitions, matrix, sequence):
	total = 0
	unique_states = set(matrix.keys())
	for first_state in unique_states:
		p_emission = emissions[(first_state, sequence[0])]
		p_transition = transitions[(u'#', first_state)]
		p_first_state = 2 ** matrix[first_state][0]
		total += forward_const * p_emission * p_transition * p_first_state

	log_total = log2(total) - log2(forward_const)
	return log_total

# Given the foward and backward matrices, add the expected counts to count_dict
def add_emissions_expected_count(count_dict, f_matrix, b_matrix, sequence, p_sequence):
	unique_states = set(f_matrix.keys())
	for i, c in enumerate(sequence):
		for s in unique_states:
			p_seq_and_state = f_matrix[s][i] + b_matrix[s][i]
			p_state_given_seq = p_seq_and_state - p_sequence
			count_dict[(s, c)] += 2 ** p_state_given_seq

# Given the foward and backward matrices, add the expected counts to count_dict
def add_transitions_expected_count(count_dict, f_matrix, b_matrix, prev_trans_dict, prev_emis_dict, sequence, p_sequence):
	unique_states = set(f_matrix.keys())
	for i,c in enumerate(sequence[1:]): #drop first char
		for t1 in unique_states:
			for t2 in unique_states:
				p_bar_t1_t2 = f_matrix[t1][i] + log2(prev_trans_dict[(t1, t2)]) + log2(prev_emis_dict[(t2, c)]) + b_matrix[t2][i + 1]
				p_t1_t2_given_bar = p_bar_t1_t2 - p_sequence
				count_dict[(t1, t2)] += 2 ** p_t1_t2_given_bar
	# count start transitions
	for t2 in unique_states:
		p_bar_t1_t2 = log2(prev_trans_dict[(u'#', t2)]) + log2(prev_emis_dict[(t2, sequence[0])]) + b_matrix[t2][0]
		p_t1_t2_given_bar = p_bar_t1_t2 - p_sequence
		count_dict[(u'#', t2)] += 2 ** p_t1_t2_given_bar

# Change expected counts to a probability distribution
def normalize(count_dict):
	prob_dict = defaultdict(float)
	all_0th_elems = set(k[0] for k in count_dict.keys())
	for e in all_0th_elems:
		total_count = 0
		for k, v in count_dict.items():
			if e is k[0]:
				total_count += v
		for k, v in count_dict.items():
			if e is k[0]:
				prob_dict[k] = v / total_count

	return prob_dict

def total_alpha(emissions, transitions, words):
	total = 0.0
	for word in words:
		w = word.split()
		f_matrix = forward(emissions, transitions, w)
		total += forward_total(f_matrix)
	return total

def pretty_print(emissions, transitions):
	em_file = open('emit-2state.txt', 'w')
	for e, p in sorted(emissions.items()):
		em_file.write(e[0] + " " + e[1] + " " + str(p) + "\n")

	trans_file = open('trans-2state.txt', 'w')
	for t, p in sorted(transitions.items()):
		trans_file.write(t[0] + " " + t[1] + " " + str(p) + "\n")

def run(initial_emissions, initial_transitions, words):
	init_alpha = total_alpha(initial_emissions, initial_transitions, words)
#	print init_alpha

	emissions = initial_emissions
	transitions = initial_transitions

	cur_alpha = init_alpha
	done = False
	while (True):
		prev_alpha = cur_alpha
		emissions_count = defaultdict(float)
		transitions_count = defaultdict(float)
		for word in words:
			w = word.split()
			f_matrix = forward(emissions, transitions, w)
			b_matrix = backward(emissions, transitions, w)
			p_w = forward_total(f_matrix)
			add_emissions_expected_count(emissions_count, f_matrix, b_matrix, w, p_w)
			add_transitions_expected_count(transitions_count, f_matrix, b_matrix, transitions, emissions, w, p_w)
		emissions = normalize(emissions_count)
		transitions = normalize(transitions_count)
		cur_alpha = total_alpha(emissions, transitions, words)
		diff = cur_alpha - prev_alpha
#		print cur_alpha, diff
		if (diff < convergence_threshold):
			return (cur_alpha, emissions, transitions)

def test():
	transitions = {}
	transitions[(u'#', u'C')] = 0.7
	transitions[(u'#', u'V')] = 0.3
	transitions[(u'C', u'C')] = 0.4
	transitions[(u'C', u'V')] = 0.6
	transitions[(u'V', u'V')] = 0.1
	transitions[(u'V', u'C')] = 0.9

	emissions = {}
	emissions[(u'C', u'b')] = 0.09
	emissions[(u'V', u'b')] = 0.01
	emissions[(u'C', u'a')] = 0.02
	emissions[(u'V', u'a')] = 0.14
	emissions[(u'C', u'r')] = 0.07
	emissions[(u'V', u'r')] = 0.03

	w = [ u'b', u'a', u'r']
	print w
	emissions_count = defaultdict(float)
	transitions_count = defaultdict(float)

	f_matrix = forward(emissions, transitions, w)
	b_matrix = backward(emissions, transitions, w)
	p_w = forward_total(f_matrix)
	add_emissions_expected_count(emissions_count, f_matrix, b_matrix, w, p_w)
	add_transitions_expected_count(transitions_count, f_matrix, b_matrix, transitions, emissions, w, p_w)
	print emissions_count
	print transitions_count



# parse transitions file into a dictionary
# key: (state_state, finish_state), value: probability of transition
def parse_transitions(file):
	text = codecs.open(file, 'r', 'utf8')
	transitions_count = defaultdict(float)
	for line in text:
		values = line.split()
		start = values[0]
		finish = values[1]
		transitions_count[(start, finish)] = random()

	return normalize(transitions_count)

# parse emissions input file
# assigns an even distribution to all possible emissions for a state
def parse_emissions(file):
	text = codecs.open(file, 'r', 'utf8')
	emission_count = defaultdict(float)
	for line in text:
		values = line.split()
		state = values[0]
		emission = values[1]
		emission_count[(state, emission)] = random()

	return normalize(emission_count)

if __name__=='__main__':
	emissions_file = sys.argv[1]
	transitions_file = sys.argv[2]
	coprus_file = sys.argv[3]

	text = codecs.open(coprus_file, 'r', 'utf8')
	words = [ w for w in text ]

	# Execute 10 times and choose the best
	results = []
	for i in range(1, 11):
		emissions_dict = parse_emissions(emissions_file)
		transitions_dict = parse_transitions(transitions_file)
		results.append(run(emissions_dict, transitions_dict, words))
		print "ITERATION " + str(i) + " DONE"

	best = max(results)
	pretty_print(best[1], best[2])

	#test()
