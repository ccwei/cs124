import os
import sys

_PLURALS = ['they', 'people']
_INFINITIVE_BE = ['might', 'to', 'can', 'could', 'should', 'shall']

# sentence = [['word1', 'pos1'], ['word2', 'pos2']]
def rule1(sentence):
	newSentence = []
	for i in range(0, len(sentence)):
		wordPos = sentence[i]
		if wordPos[1] == 'JJS' or wordPos[1] == 'RBS':
			newSentence.append(['the', 'DT'])
		newSentence.append(wordPos)
	return newSentence


def rule2(sentence):
	newSentence = []
	for i in range(0, len(sentence)):
		wordPos = sentence[i]
		prevWordPos = []
		modifiedWord = ''
		if i > 0:
			prevWordPos = sentence[i-1]

		if wordPos[0].lower() == 'be' and wordPos[1] == 'VB':
			if not prevWordPos[0].lower() in _INFINITIVE_BE:
				start = max(-3, -1*i)
				end = min(3, len(sentence)-i)
				for j in range(start, end):
					windowWordPos = sentence[i+j]
					if windowWordPos[1] == 'PRP':
						if windowWordPos[0].lower() in _PLURALS:
							modifiedWord = 'are'
							break
					elif windowWordPos[1] == 'NNS':
						modifiedWord = 'are'
						break
					else:
						modifiedWord = 'is'

				wordPos = [modifiedWord, 'VB']

				if prevWordPos[0].lower() == 'not' and prevWordPos[1] == 'RB':
					newSentence[-1] = wordPos
					wordPos = prevWordPos
		
		newSentence.append(wordPos)
	return newSentence

def rule3(sentence):
	newSentence = []
	for i in range(0, len(sentence)):
		print "TODO"
	return newSentence

def rule4(sentence):
	newSentence = []
	for i in range(0, len(sentence)):
		wordPos = sentence[i]
		prevWordPos = []
		modifiedWord = ''

		if i > 1:
			prevWordPos = sentence[i-1]

			if wordPos[1][:2] == 'JJ' and prevWordPos[1][:2] == 'NN':
				if wordPos[0] != 'NULL' and prevWordPos[0] != 'NULL':
					newSentence[-1] = wordPos
					wordPos = prevWordPos

		newSentence.append(wordPos)	
	return newSentence

def rule12(sentence):
	newSentence = []
	for i in range(0, len(sentence)):
		wordPos = sentence[i]
		prevWordPos = []
		modifiedWord = ''

		if i > 1:
			prevWordPos = sentence[i-1]

			if wordPos[1][:2] == 'VB' and prevWordPos[1][:2] == 'VB':
				if wordPos[0] != 'NULL' and prevWordPos[0] != 'NULL':
					toWordPos = ['to', 'TO']
					newSentence.append(toWordPos)

		newSentence.append(wordPos)	
	return newSentence
#sentence = [['but', 'CC'], ['expert', 'NN'], ['say', 'VBP'], [',', ','], ['they', 'PRP'], ['not', 'RB'], ['be', 'VB'], ['dreary', 'JJ'], ['or', 'CC'], ['no', 'DT'], ['more', 'JJR'], ['use', 'NN'], [',', ','], ['merely', 'RB'], ['temporary', 'JJ'], ['give', 'VBP'], ['individual', 'NN'], ['gasp', 'VB'], ['for', 'IN'], ['breath', 'NN'], ['NULL', 'NN'], ['space', 'NN']]
#sentence = [['despite', 'IN'], ['Facebook', 'NNP'], ['is', 'VBZ'], ['currently', 'RB'], ['all', 'DT'], ['beautiful', 'JJ'], ['most', 'JJS'], ['bear', 'NN'], ['welcome', 'JJ'], ['NULL', 'NN'], ['social', 'JJ'], ['network', 'NN'], ['website', 'NN'], [',', ','], ['it', 'PRP'], ['attract', 'VBP'], ['already', 'RB'], ['approximately', 'RB'], ['two-thirds', 'JJ'], ['NULL', 'JJ'], ['adult', 'JJ'], ['people', 'NNS'], ['flow', 'VBP'], ['even', 'RB'], ['forget', 'VB'], ['return', 'NN']]

#sentence = rule4(sentence)
#print sentence		