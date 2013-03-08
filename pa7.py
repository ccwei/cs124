import commands
from apply_rules import *
from andyrules import *

f = open('dic', 'r')
paragraph = open('paragraph.txt', 'r')
dic = {}
for line in f:
  parts = line.decode('utf-8').rstrip().split(' ')
  dic[parts[0]] =" ".join(parts[1:])
f.close()

text = paragraph.read().decode('utf-8').rstrip()

def checkPrefix(dic, word):
  for w in dic:
   if w.startswith(word):
     return True

  return False

idx = 0
current = 0
translation = ""

while idx < len(text) - 1:
  #print 'idx = ', idx, 'current = ', current
  while(checkPrefix(dic, text[idx:current + 1])):
    current += 1
  #print text[idx: current]
  if text[idx: current] in dic:
    #print text[idx:current].encode('utf-8'), 'in dic'
    #print dic[text[idx: current]].encode('utf-8')

    translation += " " + dic[text[idx: current]]

  if current == idx: #text[idx: current + 1] is not in dictionary
    idx += 1
    current += 1
  else:
    idx = current #start from text[current: ]

translation = translation.encode('utf-8')
#print translation

print translation
f = open('out.txt', 'w')
f.write(translation)
f.close()

commands.getoutput('./stanford-postagger.sh ./stanford-postagger/models/english-bidirectional-distsim.tagger ./out.txt > pos.txt')

f = open('pos.txt', 'r')
pos = f.read()
#print pos
#print text
#print len(text)
#print dic
