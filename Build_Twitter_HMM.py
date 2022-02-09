import json
#-*- coding: utf-8 -*-
g = open("twt.train.json", "r")
i = 0
S = []
O = []
Trans_matrix = {}
Emmis_matrix = {}
Trans_from = {}
State_count = {}
S.append('<S>')


def update_trans_from(s):
    if s != '<E>': # S != '<S>'
        if s in Trans_from.keys():
            Trans_from[s] += 1
        else:
            Trans_from[s] = 1


def update_trans_matrix(s, prev_state):
    if (s, prev_state) in Trans_matrix.keys():
        Trans_matrix[(s, prev_state)] += 1
    else:
        Trans_matrix[(s, prev_state)] = 1
    update_trans_from(prev_state)


def update_state_count(s):
    if s in State_count.keys():
        State_count[s] += 1
    else:
        State_count[s] = 1


def update_emission_matrix(o, s):
    if (o, s) in Emmis_matrix.keys():
        Emmis_matrix[(o, s)] += 1
    else:
        Emmis_matrix[(o, s)] = 1
    update_state_count(s)


for data in g:
    line = json.loads(data) # line is a list of lists
    Prev_state = '<S>'
    state = '<S>'
    obs = None
    for word in line: # word is a list of obs, state
        obs = word[0].capitalize()
        state = word[1]
        if obs not in O:
            O.append(obs)
        if state not in S:
            S.append(state)
        update_trans_matrix(state, Prev_state)
        update_emission_matrix(obs, state)
        Prev_state = state
    update_trans_matrix('<E>', Prev_state)
    update_trans_from(Prev_state)

if 'M' not in S:
    S.append('M')
S.append('<E>')
write_file = open('Twitter_POS_HMM.py', 'w', encoding="utf-8")
for s in S:
    for s1 in S:
        if s != '<S>' and s1 != '<E>':
            if (s, s1) in Trans_matrix.keys():
                if s1 not in Trans_from.keys():
                    Trans_matrix[(s, s1)] = 0
                else:
                    Trans_matrix[(s, s1)] = float(Trans_matrix[(s, s1)] * 1.0) / float(Trans_from[s1])
            else:
                Trans_matrix[(s, s1)] = 0
    for o in O:
        if s != '<S>' and s != '<E>':
            if (o, s) in Emmis_matrix.keys():
                if s not in State_count.keys():
                    Emmis_matrix[(o, s)] = 0
                else:
                    Emmis_matrix[(o, s)] = float(Emmis_matrix[(o, s)]*1.0)/State_count[s]
            else:
                Emmis_matrix[(o, s)] = 0
    # need to divide all the probabilities to get proper values properly

SEQUENCE = ['RT', '@britinho_06', ':', '@cremetroye', 'omg', 'so', 'cute']
write_file.write("# -*- coding: utf-8 -*-")
write_file.write("\n")
#write_file.write("S = " + str(S))
write_file.write("S = ['N', 'O', 'S', '^', 'Z', 'L', 'M', 'V', 'A', 'R', '!', 'D',\
     'P', '&', 'T', 'X', 'Y', '#', '@', '~', 'U', 'E', '$', ',', 'G']")
write_file.write("\n")
write_file.write("O = " + str(O))
write_file.write("\n")
write_file.write("P_trans = " + str(Trans_matrix))
write_file.write("\n")
write_file.write("P_emission =" + str(Emmis_matrix))
write_file.write("\n")
write_file.write("SAMPLE_OBS_SEQ =" + str(SEQUENCE))
write_file.write("\n")
write_file.write("if __name__=='__main__':")
write_file.write("\n\t")
write_file.write("import HMM_vis as hv")
write_file.write("\n\t")
write_file.write("hv.show_entire_trellis(S, SAMPLE_OBS_SEQ,1500,800,True)")
write_file.write("\n\t")
