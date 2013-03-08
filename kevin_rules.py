import os
import sys
import copy

#3 - get rid of space between digits
#5 - Pluralize NN if it follow "2" (or more), "those", "these"
#7 - Pronoun + NULL => Possessive (I -> my, He/ She -> his/her)
#8 - JJ VB => RB VB (ex: temporary_JJ give_VBP -> temporarily give)
#9 - "have" (VB) in the beginning of the sentence or after comma or semicolon or conjunction -> there is/are (depends on whether we next have NN/NNP or NNS/NNPS in sentence - if we have neither then we go with "is" by default)

pronoun_possession_dict = {"I" : "my", "you" : "your", "they" : "their", "we" : "our", "he" : "his", "she" : "her"}
third_person_pronoun_set = set(['he', 'she', 'it'])
pronoun_set = set(['I', 'you', 'he', 'she', 'it', 'they', 'we'])

def is_at_least_two(token):
	return token[1] == "CD" and token[0] not in ["one", "1"]

def pluralize(word):
	assert(len(word) > 0)
	if word[-1] == 's':
		word += "es"
	else:
		word += "s"

	return word

def adverbify(word):
	assert(len(word) > 0)
	if word[-1] == 'y':
		word = word[:-1] + "ily"
	else:
		word += "ly"

	return word

def rule5(sentence):
	new_sentence = copy.deepcopy(sentence)
	for i in xrange(1, len(new_sentence)):
		if new_sentence[i][0] != "NULL" and new_sentence[i][1] == "NN" and (is_at_least_two(new_sentence[i - 1]) or new_sentence[i - 1][0] in ["these", "those"]):
			new_sentence[i][0] = pluralize(new_sentence[i][0])

	return new_sentence

def rule7(sentence):
	new_sentence = []
	just_applied_rule = 0
	for i in xrange(len(sentence)):
		if just_applied_rule:
			just_applied_rule = 0
			continue

		if i == len(sentence) - 1:
			new_sentence.append(sentence[i])
			continue

		if sentence[i][0] in pronoun_possession_dict and sentence[i + 1][0] == "NULL":
			just_applied_rule = 1
			new_sentence.append([pronoun_possession_dict[sentence[i][0]], "PRP$"])
		else:
			new_sentence.append(sentence[i])

	return new_sentence

def rule8(sentence):
	new_sentence = copy.deepcopy(sentence)
	for i in xrange(len(new_sentence) - 1):
		if new_sentence[i][1] == "JJ" and new_sentence[i + 1][1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
			new_sentence[i][0] = adverbify(new_sentence[i][0])
			new_sentence[i][1] = "RB"

	return new_sentence

def conjugate(word):
	assert(len(word) > 0)
	if word[-1] == 's':
		word = word[:-1] + "es"
	else:
		word += "s"

	return word

def rule11(sentence):
	new_sentence = copy.deepcopy(sentence)
	for i in xrange(len(new_sentence) - 1):
		if new_sentence[i][1] == "PRP" and new_sentence[i + 1][1] in ["VB", "VBP"]:
			print new_sentence[i][0], new_sentence[i + 1][0]
			new_sentence[i + 1][0] = conjugate(new_sentence[i + 1][0])
			new_sentence[i + 1][1] = "VBP"

	return new_sentence


def rule3(sentence):
	new_sentence = []
	just_applied_rule = 0
	for i in xrange(len(sentence)):
		if just_applied_rule > 0:
			just_applied_rule -= 1
			continue

		if i == len(sentence) - 1:
			new_sentence.append(sentence[i])
			continue

		if sentence[i][0].isdigit() and sentence[i + 1][0].isdigit():
			k = i + 1
			for j in xrange(i, len(sentence)):
				k = j
				if not sentence[j][0].isdigit():
					break

			new_sentence.append(["".join([t[0] for t in  sentence[i:k]]), "CD"])
			just_applied_rule = k - i - 1
		else:
			new_sentence.append(sentence[i])

	return new_sentence

def rule9(sentence):
	new_sentence = []
	for i in xrange(len(sentence)):
		if sentence[i][0] == "have" and sentence[i][1] in ["VB", "VBP"]:
			if i == 0 or (sentence[i - 1][0] in [",", ";"] or sentence[i - 1][1] == "CC"):
				new_sentence.append(["there", "EX"])
				is_token = ["is", "VBZ"]
				are_token = ["are", "VBP"]
				token_to_use = is_token
				for j in xrange(i + 1, len(sentence)):
					if sentence[j][1] in ["NN", "NNP"]:
						token_to_use = is_token
						break
					elif sentence[j][1] in ["NNS", "NNPS"]:
						token_to_use = are_token
						break

				new_sentence.append(token_to_use)

			else:
				new_sentence.append(sentence[i])

		else:
			new_sentence.append(sentence[i])

	return new_sentence

def moveWP(sentence):
  tmp_sentence = copy.deepcopy(sentence)
  new_sentence = []
  pronoun = -1
  delete_idx = []
  for i in xrange(len(sentence)):
    if sentence[i][0] in pronoun_set:
      pronoun = i
      break

  for i in xrange(len(sentence)):
    if sentence[i][1] in ["WP", "WRB"]:
      new_sentence.append(sentence[i])
      delete_idx.append(i)
      if i + 1 < len(sentence) and sentence[i+1][1] in ["RB"]:
        new_sentence.append(sentence[i + 1])
        delete_idx.append(i + 1)

      if i > 0 and sentence[i - 1][1] in ["VB", "VBP"]:
        new_sentence.append(["do", "DO"])
        if pronoun != -1:
          new_sentence.append(sentence[pronoun])
          delete_idx.append(pronoun)
        new_sentence.append(sentence[i - 1])
        delete_idx.append(i- 1)
        break
  delete_idx.sort(reverse=True)
  for i in xrange(len(delete_idx)):
    tmp_sentence.pop(delete_idx[i])
  for i in xrange(len(tmp_sentence)):
    new_sentence.append(tmp_sentence[i])
  return new_sentence

