from HMM_Algorithms import viterbi_algorithm
#-*- coding: utf-8 -*-
obs_sequence = ['That','cardboard','has','a', 'stick', 'in', 'it']
check = viterbi_algorithm(obs_sequence, False)
print(check)
