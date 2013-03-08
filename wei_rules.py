import os
import sys
import copy

third_person_pronoun_set = set(['he', 'she', 'it'])
pronoun_set = set(['I', 'you', 'he', 'she', 'it', 'they', 'we', 'my', 'your', 'his', 'her', 'their', 'our'])


def method_names():
  return ["rule11", "moveWP", "adjNull"]

def conjugate(word):
	assert(len(word) > 0)
	if word[-1] == 's':
		word = word[:-1] + "es"
	else:
		word += "s"

	return word

def rule11(sentence):
  new_sentence = copy.deepcopy(sentence)
  for i in xrange(len(new_sentence) - 2):
    if new_sentence[i][1] == "PRP" and new_sentence[i + 1][1] in ["VB", "VBP"]:
      if new_sentence[i][0] in third_person_pronoun_set:
        new_sentence[i + 1][0] = conjugate(new_sentence[i + 1][0])
        new_sentence[i + 1][1] = "VBZ"
    if new_sentence[i][1] == "PRP" and new_sentence[i + 2][1] in ["VB", "VBP"]:
      if new_sentence[i][0] in third_person_pronoun_set:
        new_sentence[i + 2][0] = conjugate(new_sentence[i + 2][0])
        new_sentence[i + 2][1] = "VBZ"
  
    if new_sentence[i][1] in ["NN", "NNP"] and new_sentence[i + 1][1] in ["VB", "VBP"]:
      new_sentence[i + 1][0] = conjugate(new_sentence[i + 1][0])
      new_sentence[i + 1][1] = "VBZ"
    if new_sentence[i][1] in ["NN", "NNP"] and new_sentence[i + 2][1] in ["VB", "VBP"]:
      new_sentence[i + 2][0] = conjugate(new_sentence[i + 2][0])
      new_sentence[i + 2][1] = "VBZ"
  return new_sentence

def adjNull(sentence):
  new_sentence = copy.deepcopy(sentence)
  delete_idx = []
  for i in xrange(len(sentence) - 1):
    if sentence[i][1] in ["JJ", "JJR", "JJS", "RB", "RBR", "RBS"] and sentence[i + 1][0] == "NULL":
      delete_idx.append(i + 1)

  delete_idx.sort(reverse=True)
  for i in xrange(len(delete_idx)):
    new_sentence.pop(delete_idx[i])

  return new_sentence


def moveWP(sentence):
  print 'sentence = ', sentence
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
