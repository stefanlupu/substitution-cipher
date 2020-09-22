#!/usr/bin/env python3
# Multi process version of the program

from src.quadgrams_score import english_quadgrams_log_probabilities
from timeit import default_timer as timer
import concurrent.futures
import random
import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz'                             # english alphabet
log_probabilities = english_quadgrams_log_probabilities()           # load the log probabilities from english quadgrams into memory

# get the encrypted message and return a lower case string 
# remove any non-alphabetical characters including spaces
def remove_punctutation(message):
    no_punctuation = ''

    for char in message:
        if char.isalpha():
            no_punctuation += char

    return no_punctuation

# return a deep copy of the given dictionary
def copy_dict(key):
    copy = {}
    for key, value in key.items():
        copy[key] = value

    return copy

# decrypt a given text using the provided key
# map every encountered character to its equivalent in the dictionary
# if the character is not in the dictionary then use that character instead
def decrypt(message, key):
    decrypted_message = ''
    for char in message:
        if char.islower():
            decrypted_message += key[char]
        elif char.isupper():
            decrypted_message += key[char.lower()].upper()              # because I am using lower case characters in my key dictionary I have to convert upper case to lower case to search them              
        else:
            decrypted_message += char

    return decrypted_message

# change the key slightly by swapping 2 random characters
def randomize_key(key):
    # copy the key into a new dictionary to ensure we do not override the original key
    shuffled_key = copy_dict(key)

    swap_1 = alphabet[random.randint(0, 25)]
    swap_2 = alphabet[random.randint(0, 25)]

    # if the 2 random numbers happen to be the same keep generating them until they are different
    if swap_1 == swap_2:
        while swap_1 == swap_2:
            swap_1 = alphabet[random.randint(0, 25)]
            swap_2 = alphabet[random.randint(0, 25)]

    tmp = shuffled_key[swap_1]
    shuffled_key[swap_1] = shuffled_key[swap_2]
    shuffled_key[swap_2] = tmp

    return shuffled_key

# generates a random key
# will be needed to start the hill climb
# after that we randomize keys rather than generate new ones from scratch
def generate_random_key():
    random_key = {}
    used = []

    for letter in alphabet:
        # generate a random letter selection from the alphabet
        selected = alphabet[random.randint(0,25)]

        # if the generated letter has not been used yet map it to a value
        if selected not in used:
            random_key[letter] = selected
            used.append(selected)
        else:
            # else if the generated letter has been used, keep generating until you have a letter that has yet to be selected
            while(selected in used):
                selected = alphabet[random.randint(0,25)]

            random_key[letter] = selected
            used.append(selected)

    return random_key

# decrypt a given message with a given key
# generate quadgrams from decrypted message
# look up each quadgrams scores in english_quadgrams_log_probabilities
# calculate the keys overall score by adding all the quadgrams scores together
def score_key(message, key):
    fitness = 0
    
    decrypted_message = decrypt(message, key)
    decrypted_message_quadgrams = generate_quadgrams(decrypted_message)

    for quadgram in decrypted_message_quadgrams:
        try:
            fitness += log_probabilities[quadgram]
        except:
            fitness += -10

    return fitness

# generate a list of quadgrams from a given message
# the message should not contain any non-alphabetical characters (this includes spaces)
def generate_quadgrams(message):
    quadgrams = []

    for i in range(4, len(message) + 1):
        quadgrams.append(message[i-4:i])

    return quadgrams

# actual cipher breaking process
# known as hill-climbing algorith
# generate a random key as the parent to begin the process
# score how effective it is at decrypting the message
# create a child by slightly modifing the parent and score it
# if the score of the child is better than the parent then update the parent
# else keep randomizing the child until a better score is achieved
# try this for 10,000 iterations
# because we will be using threads in main() we don't need to run the cipher crack 4 times here
def crack_cipher(message):

    parent = generate_random_key()
    child = randomize_key(parent)

    i = 0
    reset = 1000
    while i < 10000:

        parent_score = score_key(message, parent)
        child_score = score_key(message, child)

        if child_score > parent_score:
            parent = copy_dict(child)
            # counter can go back to its original value since a change to the parent has been made
            reset = 1000
        else:
            child = randomize_key(parent)
            # decrement the counter as no change to the parent has been made
            reset -= 1

        # if no change has appeared in the parent in the last 1000 iterations then randomize the parent
        if reset is 0:
            parent = randomize_key(parent)

        i += 1

    return parent, parent_score


def main(file=None):
    # get the file containint the encrypted message
    if file is None:
        input_file = sys.argv[1]
    else:
        # a file is given to main when ever I use my testing program
        input_file = file

    with open(input_file, 'r') as f:
        original = f.read().strip()

    # format the input
    message = remove_punctutation(original)

    start = timer()

    # decrypt the key
    solution_scores = []
    threads = []
    solutions = {}

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # start all the processes
        for i in range(4):
            threads.append(executor.submit(crack_cipher, message))

        # store the return values of each thread as they complete their task
        for thread in concurrent.futures.as_completed(threads):
            key, score = thread.result()
            solution_scores.append(score)
            solutions[score] = key

    # the best key is the one with the greatest score
    decryption_key = solutions[max(solution_scores)]
    
    end = timer()

    # write the key as well as the decoded message to files based on the name of the input file
    output_file = input_file[:-4] + '-decrypted.txt'
    with open(output_file, 'w') as o:
        o.write(decrypt(original, decryption_key) + '\n')


    output_key = input_file[:-4] + '-key.txt'
    with open(output_key, 'w') as o:
        o.write("letter = cypher-letter\n\n")
        for key, value in sorted(decryption_key.items()):
            o.write(f'{key} = {value}\n')

    return end - start

if __name__ == '__main__':
    main()
