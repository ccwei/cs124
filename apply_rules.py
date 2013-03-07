import os
import sys

def process_pos_file(pos_filename):
	f = open(pos_filename, "r")
	lines = [line.rstrip() for line in f]
	all_text = " ".join(lines)
	tokens = all_text.split(" ")
	print(tokens)
	sentences = [[]]
	for token in tokens:
		if token.split("_")[1] == ".":
			sentences.append([])
		elif len(token) > 0:
			sentences[-1].append(token.split("_"))

	return sentences


if __name__ == "__main__":
	pos_filename = sys.argv[1]
	sentences = process_pos_file(pos_filename)
	print len(sentences)
	for sentence in sentences:
		print(sentence)
