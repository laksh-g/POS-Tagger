import json
from HMM_Algorithms import viterbi_algorithm
#-*- coding: utf-8 -*-
g = open("twt.test.json", "r")

TOTAL_WORDS = 0
TOTAL_CORRECT = 0

for data in g:
    line = json.loads(data) # line is a list of lists
    obs_sequence = []
    ans_sequence = []
    for word in line: # word is a list of obs, state
        obs = word[0]
        state = word[1]
        TOTAL_WORDS += 1
        obs_sequence.append(obs)
        ans_sequence.append(state)
    check = viterbi_algorithm(obs_sequence, False)

    for i in range(len(obs_sequence)):
        if check[i] == ans_sequence[i]:
            TOTAL_CORRECT += 1

correct_prec = (float(TOTAL_CORRECT)/TOTAL_WORDS)*100
print("Test set accuracy = " + str(correct_prec))
print("Total count of correctly tagged words = " + str(TOTAL_CORRECT))
print("Total count of words = " + str(TOTAL_WORDS))


