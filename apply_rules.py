import os
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
		if token.split("_")[1] == ".":
			sentences[-1].append(['.', '.'])
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

  print rules
  translated_sentence = []
  for sentence in sentences:
    for key in ['kevin_rules', 'wei_rules', 'andyrules']: #ensure the sequence of the rule applying
      print key
      imported_module = importlib.import_module(key)
      for r in rules[key]:
		    sentence = getattr(imported_module, r)(sentence)
    translated_sentence += sentence
  print translated_sentence
  print " ".join([word[0] for word in translated_sentence])
	  #print '--', sentence
		#print getattr(wei_rules, 'moveWP')(sentence)
