import codecs
import sys

def transitions(file):
	text = codecs.open(file, 'r', 'utf8')
	transitions_dict = {}
	for line in text:
		values = line.split()
		start = values[0]
		finish = values[1]
		prob = values[2]

		start_dict = transitions_dict.get(start, None)
		if start_dict is None:
			start_dict = {}
			transitions_dict[start] = start_dict
		start_dict[finish] = prob
	return transitions_dict



if __name__=='__main__':
	emissions_file = sys.argv[1]
	observation_file = sys.argv[2]
	transitions_file = sys.argv[3]

	print transitions(transitions_file)

