import os
import re
import sys
import wei_rules
import kevin_rules
import andyrules
import importlib

def process_pos_file(pos_filename):
	f = open(pos_filename, "r")
	lines = [line.rstrip() for line in f]
	all_text = " ".join(lines)
	tokens = all_text.split(" ")
	print(tokens)
	sentences = [[]]
	for token in tokens:
		if token.split("_")[1] in [".", ",", "?"]:
			sentences[-1].append([token.split("_")[0], token.split("_")[0]])
			sentences.append([])
		elif len(token) > 0:
			sentences[-1].append(token.split("_"))
	return sentences

if __name__ == "__main__":
  pos_filename = sys.argv[1]
  sentences = process_pos_file(pos_filename)
  print len(sentences)
  rules = {}
  rules['andyrules'] = (getattr(andyrules, 'method_names')())
  rules['kevin_rules'] = (getattr(kevin_rules, 'method_names')())
  rules['wei_rules'] = (getattr(wei_rules, 'method_names')())

  translated_sentence = []
  for sentence in sentences:
    for key in ['kevin_rules', 'wei_rules', 'andyrules']: #ensure the sequence of the rule applying
      imported_module = importlib.import_module(key)
      for r in rules[key]:
		    sentence = getattr(imported_module, r)(sentence)
    translated_sentence += sentence
  #Capitalize
  translated_sentence[0][0] = translated_sentence[0][0].capitalize()
  for i in xrange(len(translated_sentence) - 1):
    if translated_sentence[i][0] == '.':
      translated_sentence[i + 1][0] = translated_sentence[i + 1][0].capitalize()
  translation = " ".join([word[0] for word in translated_sentence])

  #Remove extra space
  translation = re.sub(' \.', '.', translation)
  translation = re.sub(' ,', ',', translation)
  translation = re.sub(' \?', '?', translation)
  translation = re.sub(' ;', ';', translation)
  print translation

