import pandas as pd
import numpy as np
import random
import math


def train_markov(lyrics, K):
    """ 
    Generate a dictionary of Kmers from a sequence of words
    lyrics is a pandas series, order is the order of the markov chain
    I want to test on 1st order, 3rd order and 5th order markov 
    chains
    """

    Kmers = {}
    num_nodes = 0
     
    for s in range(len(lyrics)):
        words = lyrics.loc[s]['lyrics'].split()

        for i in range(len(words)-K):
            #node = words[i:(i+K)]
            node = ''
            for j in range(i, i+K):
                node = node + words[j] + " " 
            if node not in Kmers:
                Kmers.update({node : 1})
                num_nodes += 1
            else:
                Kmers[node] += 1
                num_nodes += 1

    for node in Kmers:
        Kmers[node] = (float(Kmers[node]) / float(num_nodes))*100
    
    return Kmers

    
def markov_poten(seq, chain, anti_chain, K):
    """
    Determines the probability that the novel sequence comes
    from a determined markov chain or its complement.
    Seq is a single song, i guess it will be a list and the chains 
    come from train_markov. K is the order of the chains
    """
    poten = np.array([])
    #need to set up initial probabilities
    node = ''
    for i in range(K):
        node = node + seq[i] + " "

    if node not in chain:
        pr_ch = 1.0
    else:
        pr_ch = float(chain[node])
    
    if node not in anti_chain:
        pr_an = 1.0
    else:
        pr_an = float(anti_chain[node])

    for i in range(1, len(seq)-K):
        node = ''
        for j in range(i, i+K):
            node = seq[j] + " "

        if node not in chain:
            pr_ch = 1.0*pr_ch
        else:
            pr_ch = pr_ch*float(chain[node])
    
        if node not in anti_chain:
            pr_an = 1.0*pr_an
        else:
            pr_an = pr_an*float(anti_chain[node])

        if pr_an == 0:
            pot = 99
            poten = np.append(poten, pot)
            continue
        try:
            pot = math.log10(pr_ch/pr_an)
        except ValueError:
            pot = 0

        poten = np.append(poten, pot)

    return poten



    
    

    
