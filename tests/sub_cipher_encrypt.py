#!/usr/bin/env python3

# encrypt files using a substitution cypher

import sys
import secrets

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def generate_key(alphabet):
    key_map = {}
    used = []

    for letter in alphabet:
        if letter not in alphabet:
            continue

        selection = secrets.choice(alphabet)

        if selection not in used:
            key_map[letter] = selection
            used.append(selection)
        else:
            while(selection in used):
                selection = secrets.choice(alphabet)

            key_map[letter] = selection
            used.append(selection)

    return key_map

def print_key(key_map):
    for key, value in key_map.items():
        print(f'Original {key} maps to {value}')

# copy the dictionary containing the key into a file
def copy_key(key_map, file_name):
    output_string = 'letter = cypher-letter\n\n'

    for key, value in key_map.items():
        output_string += '   ' + str(key) + '           ' + str(value) + '\n'

    with open(file_name, 'w') as f:
        f.write(output_string)


def reverse_dictionary(dict):
    reversed = {}

    for key, value in dict.items():
        reversed[value] = key

    return reversed

def encrypt(words, key):
    encrypted = []
    tmp = ''

    for word in words:
        for letter in word:
            if letter.islower():
                tmp += key[letter]
            elif letter.isupper():
                tmp += key[letter.lower()].upper()
            elif letter not in alphabet:
                tmp += letter
                
        encrypted.append(tmp)
        tmp = ''

    return encrypted

def main(file=None):
    # get the file containing the encrypted message
    if file is None:
        input_file = sys.argv[1]
    else:
        # a file is given to main when ever I use my testing program
        input_file = file

    with open(file, 'r') as f:
        words = "".join(f.read()).split()

    key_map = generate_key(alphabet)
    copy_key(key_map, 'og-encryption-key.txt')

    encrypted = encrypt(words, key_map)
    decrypted = encrypt(encrypted, reverse_dictionary(key_map))

    with open('encrypted-message.txt', 'w') as f:
        f.write(" ".join(encrypted))

if __name__ == '__main__':
    main()
