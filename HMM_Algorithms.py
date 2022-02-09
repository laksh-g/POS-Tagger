'''HMM_Algorithms.py

by Laksh Gupta

Date: 05/27/2020

for CSE 473 Assignment 7, Spring 2020
University of Washington.

Provide your own implementations of the Forward Algorithm
and the Viterbi Algorithm in the provided function templates.

Your Forward Algorithm should compute the belief vector B_t at each
point t in time.  Here B_t(s) = P(S_t=s | E_1=e_1, E_2=e_2, ..., E_t=e_t)
Here E_t represents the emission at time step t, etc.
For the Toy_POS_tagger, it should display the belief values next
to each of the nodes.

Your Viterbi Algorithm should for each node the probability of reaching
that node from the start along the most probable path.
For the Toy_POS_tagger, it should display this probability next
to each of the nodes, and it should highlight the (or a) most probable path.

'''

import HMM_vis as hv
#import Toy_POS_tagger as theHMM
import Twitter_POS_HMM as theHMM

OBSERVATION_SEQUENCE = theHMM.SAMPLE_OBS_SEQ
PREV_BELIEF_VALUES = {}
INT_BELIEF_VALUES = {}
BACKTRACK = []

TIME = 1
def fa_one_state_advance_time(s):
    new_val = 0
    for s1 in PREV_BELIEF_VALUES.keys():
        if TIME == 1:
            if s1 != '<E>':
                new_val += float(theHMM.P_trans[(s, s1)])*PREV_BELIEF_VALUES[s1]
        else:
            if s1 != '<E>' and s1 != '<S>':
                new_val += float(theHMM.P_trans[(s, s1)])*PREV_BELIEF_VALUES[s1]
    # Put your code here.
    return new_val



def fa_one_state_observe_emission(s, e):
    # Put your code here.
    if (e, s) in theHMM.P_emission:
        return float(fa_one_state_advance_time(s)) * theHMM.P_emission[(e, s)]
    else:
        return float(va_one_state_advance_time(s))*0.0005

def fa_finish_time_step(e):
    # Put your code here.
    new_belief_vals={}
    for s in theHMM.S:
        if s != '<S>' and s != '<E>':
            val = fa_one_state_observe_emission(s, e)
            INT_BELIEF_VALUES[s] = val

    belief_sum = sum(INT_BELIEF_VALUES.values())
    for s in theHMM.S:
        if s != '<S>' and s != '<E>':
            val = float(INT_BELIEF_VALUES[s])/belief_sum
            new_belief_vals[s] = val
    return new_belief_vals



def forward_algorithm(obs_sequence, show=False):

    global TIME, BELIEF, PREV_BELIEF_VALUES

    if show:
        hv.show_entire_trellis(theHMM.S, obs_sequence, has_initial_state=True)
        hv.highlight_node(0, '<S>', highlight=True) # Demo of node highlighting.
        # highlight/unhighlight other nodes as appropriate
        # to show progress.

    resultList =[]
    PREV_BELIEF_VALUES['<S>'] = 1
    PREV_BELIEF_VALUES['N'] = 0
    PREV_BELIEF_VALUES['M'] = 0
    PREV_BELIEF_VALUES['V'] = 0
    PREV_BELIEF_VALUES['<E>'] = 0
    resultList.append(PREV_BELIEF_VALUES.values())
    for o in obs_sequence:
        new_dict = fa_finish_time_step(o.capitalize())

        for s in PREV_BELIEF_VALUES.keys():
            if s != '<S>' and s != '<E>':
                PREV_BELIEF_VALUES[s] = new_dict[s]
        resultList.append(PREV_BELIEF_VALUES.values())
        for s in theHMM.S:
            if s != '<S>' and s != '<E>':
                hv.show_label_at_node(TIME, s, str(PREV_BELIEF_VALUES[s]), 0, -30)
        TIME+=1
        #print(resultList)
    return resultList

    # Put your code here, making calls to the various fa_* functions you wrote.
    # When debugging, use calls to highlight_node and show_node_label
    # to illustrate the progress of your algorithm.

def va_one_state_advance_time(s):
    global TIME, BACKTRACK
    max_val = 0.0
    if TIME == 1:
        max_val = float(theHMM.P_trans[(s, '<S>')]) * PREV_BELIEF_VALUES['<S>']
        BACKTRACK[TIME][s] = '<S>'
    else:
        for s1 in PREV_BELIEF_VALUES.keys():
            if s1 != '<E>' and s1 != '<S>':
                value = float(theHMM.P_trans[(s, s1)])*PREV_BELIEF_VALUES[s1]
                if float(theHMM.P_trans[(s, s1)])*PREV_BELIEF_VALUES[s1] > max_val:
                    max_val = float(theHMM.P_trans[(s, s1)])*PREV_BELIEF_VALUES[s1]
                    BACKTRACK[TIME][s] = s1
    return max_val

def va_one_state_observe_emission(s, e):
    if (e, s) in theHMM.P_emission:
        return float(va_one_state_advance_time(s)) * theHMM.P_emission[(e, s)]
    else:
        return float(va_one_state_advance_time(s))*0.0005

def va_finish_time_step(e):
    new_belief_vals = {}
    for s in theHMM.S:
        if s != '<E>' and s != '<S>':
            val = va_one_state_observe_emission(s, e)
            new_belief_vals[s] = val
    return new_belief_vals

def viterbi_algorithm(obs_sequence, show=False):
    global TIME
    if show:
        hv.show_entire_trellis(theHMM.S, obs_sequence, has_initial_state=True)
        hv.highlight_node(0, '<S>')
        hv.highlight_node(len(obs_sequence), '<E>')

        # highlight other nodes and edges as appropriate
        # to show progress and results.

    resultList = []

    for s in theHMM.S:
        PREV_BELIEF_VALUES[s] = 0
    PREV_BELIEF_VALUES['<S>'] = 1
    BACKTRACK.append({})
    for o in obs_sequence:
        BACKTRACK.append({})
        new_dict = va_finish_time_step(o.capitalize())
        for s in PREV_BELIEF_VALUES.keys():
            if s != '<S>' and s != '<E>':
                PREV_BELIEF_VALUES[s] = new_dict[s]
        for s in theHMM.S:
            if show:
                if s != '<S>' and s != '<E>':
                    hv.show_label_at_node(TIME, s, str(PREV_BELIEF_VALUES[s]), 0, -18)
        TIME += 1

    maxs = '<S>'
    maxv = 0
    TIME -= 1
    for s in PREV_BELIEF_VALUES.keys():
        if s != '<S>' and s != '<E>':
            if PREV_BELIEF_VALUES[s] > maxv:
                maxv = PREV_BELIEF_VALUES[s]
                maxs = s
    #print(BACKTRACK)
    #print(maxs)
    resultList.append(maxs)
    while maxs != '<S>':
        resultList.insert(0, BACKTRACK[TIME][maxs])
        maxs = resultList[0]
        TIME -= 1

    #print(resultList)
    if show:
        for i in range(len(resultList)-1):
            hv.highlight_edge(i, resultList[i], resultList[i+1])
            hv.highlight_node(i+1, resultList[i+1])
        hv.highlight_edge(len(resultList)-1, resultList[-1], '<E>')
    resultList.remove('<S>')

    #print(resultList)
    TIME = 1
    return resultList


    # Put your code here, making calls to the various va_* functions you wrote.
    # When debugging, use calls to highlight_node, highlight_edge,
    # and show_node_label to illustrate the progress of your algorithm.

#forward_algorithm(OBSERVATION_SEQUENCE, show=True)
#viterbi_algorithm(OBSERVATION_SEQUENCE, show=True)

    
