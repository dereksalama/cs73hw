# Derek Salama
# CS 73
# 10/11/2013

import codecs
import sys
from math import log

# scale all probabilities to prevent underflow
forward_const = 10000000.0
def forward(emissions, transitions, sequence):
	unique_states = set(key[0] for key in emissions.keys())

	matrix = {state: [] for state in unique_states}

	# Initialize: fill out first column
	for state in unique_states:
		p_s = transitions[("#", state)]
		p_w = emissions[(state, sequence[0])]
		matrix[state].append(p_s * p_w * forward_const)

	# General Case
	# Loop through observation
	for (i, c) in enumerate(sequence[1:], start=1):
		total = 0
		# loop through each state for given observation
		for current_state in unique_states:
			p_emission = emissions[(current_state, c)]
			total_prob = 0
			# Inner loop: all possible previous states
			for previous_state in unique_states:
				p_transition = transitions[(previous_state, current_state)]
				p_previous_state = matrix[previous_state][i-1]
				total_prob += p_previous_state * p_emission * p_transition
			matrix[current_state].append(total_prob)

	# divide by constant to get correct answer
	for l in matrix.values():
		for (i, p) in enumerate(l):
			l[i] = p / forward_const

	# sum final column
	total = sum(l[-1] for l in matrix.values())
	print "Foward: " + str(total)

def log2(n):
	return log(n, 2)

def viterbi(emissions, transitions, sequence):
	unique_states = set(key[0] for key in emissions.keys())

	matrix = {state: [] for state in unique_states}
	# Initialize first column
	for state in unique_states:
		p_s = transitions[("#", state)]
		p_w = emissions[(state, sequence[0])]
		p = log2(p_s) + log2(p_w)
		matrix[state].append(("#", p))

	# General case: iterate through observation
	for (i, c) in enumerate(sequence[1:], start=1):
		# loop throigh each state for a given observation
		for current_state in unique_states:
			# use logs for probabilities to prevent underflow
			p_emission = log2(emissions[(current_state, c)])
			max_prob = None
			max_previous_state = None
			#  loop through all possible previous states
			for previous_state in unique_states:
				p_transition = log2(transitions[(previous_state, current_state)])
				p_previous_state = matrix[previous_state][i-1][1]
				p = p_previous_state + p_transition + p_emission
				# only record the greatest probability
				if (p > max_prob):
					max_previous_state = previous_state
					max_prob = p
			# save tuple (source state, probability)
			matrix[current_state].append((max_previous_state, max_prob))

	categories = []

	# Find state with the greatest probability in last column
	max_p = None
	max_state = None
	for s in unique_states:
		if matrix[s][-1][1] > max_p:
			max_p = matrix[s][-1][1]
			max_state = s
	categories.append(max_state)

	# "Walk" through table, folliwing the source state in our tuples
	for i in range(len(matrix[max_state]) - 1, 0, -1):
		max_state = matrix[max_state][i][0]
		categories.append(max_state)
	categories.reverse()
	print "viterbi: " + "".join(categories)

# parse transitions file into a dictionary
# key: (state_state, finish_state), value: probability of transition
def transitions(file):
	text = codecs.open(file, 'r', 'utf8')
	transitions_dict = {}
	for line in text:
		values = line.split()
		start = values[0]
		finish = values[1]
		prob = float(values[2])
		transitions_dict[(start, finish)] = prob

	return transitions_dict

# parse emissions file into dictionary
# key: (state, emission), value: emission_probability
def emissions(file):
	text = codecs.open(file, 'r', 'utf8')
	emissions_dict = {}
	for line in text:
		values = line.split()
		state = values[0]
		emission = values[1]
		prob = float(values[2])
		emissions_dict[(state, emission)] = prob

	return emissions_dict

if __name__=='__main__':
	emissions_file = sys.argv[1]
	observation_file = sys.argv[2]
	transitions_file = sys.argv[3]

	emissions_dict = emissions(emissions_file)
	transitions_dict = transitions(transitions_file)
	sequence = codecs.open(observation_file, 'r', 'utf8').next().split()

	forward(emissions_dict, transitions_dict, sequence)
	viterbi(emissions_dict, transitions_dict, sequence)