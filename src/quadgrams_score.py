#!/usr/bin/env python3

import math

# calculate the log probability of each quadgram found in the english language
# return a dictionary containing the quadgrams and their respective log probability as key, value pairs
def english_quadgrams_log_probabilities():

    # open the file containing the quadgrams and load them to memory
    with open('../src/quadgrams.txt', 'r') as f:
        # a list containing each line of the input file 
        raw_text = f.read().split('\n')

    # convert the raw text into a dictionary containing the respective quadgrams and their count
    quadgrams_count = {}
    
    for line in raw_text:
        key, value = line.split()
        quadgrams_count[key.lower()] = int(value)

    sample_size = sum(quadgrams_count.values())

    # convert the count of each quadgram to a log probability
    quadgrams_log_probabilities = {}
    for key, value in quadgrams_count.items():
        quadgrams_log_probabilities[key] = math.log10(float(value / sample_size)) 

    return quadgrams_log_probabilities
