'''Toy_POS_tagger.py

This is an HMM to demonstrate simple Part-Of-Speech tagging.
It comes from: https://www.youtube.com/watch?v=mHEKZ8jv2SY

'''
S = ['<S>', 'N', 'M', 'V', '<E>']

O = ['Mary', 'Jane', 'Will', 'Spot', 'Can', 'See', 'Pat']

# P_trans[('N','V')] gives P(S_t = 'N' | S_{t-1} = 'V')
P_trans={('N','<S>'):3/4,
         ('M','<S>'):1/4,
         ('V','<S>'):0,
         ('<E>','<S>'):0,

         ('N','N'):1/9,
         ('M','N'):1/3,
         ('V','N'):1/9,
         ('<E>','N'):4/9,

         ('N','M'):1/4,
         ('M','M'):0,
         ('V','M'):3/4,
         ('<E>','M'):0,

         ('N','V'):1,
         ('M','V'):0,
         ('V','V'):0,
         ('<E>','V'):0}

P_emission={('Mary','N'):4/9, ('Mary','M'):0, ('Mary','V'):0,
       ('Jane','N'):2/9, ('Jane','M'):0, ('Jane','V'):0,
       ('Will','N'):1/9, ('Will','M'):3/4, ('Will','V'):0,
       ('Spot','N'):2/9, ('Spot','M'):0, ('Spot','V'):1/4,
       ('Can','N'):0, ('Can','M'):1/4, ('Can','V'):0,
       ('See','N'):0, ('See','M'):0, ('See','V'):1/2,
       ('Pat','N'):0, ('Pat','M'):0, ('Pat','V'):1/4}

SAMPLE_OBS_SEQ = ['Jane','will','spot','Will']

if __name__=='__main__':
    import HMM_vis as hv
    hv.show_entire_trellis(S, SAMPLE_OBS_SEQ,3000,1000,True)
    
