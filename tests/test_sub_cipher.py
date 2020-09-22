#!/usr/bin/env python3
# Program I used to test my main programs


import sys
sys.path.append('../')
from src.single_sub_cipher_decrypt import main as single_decrypt
from src.multi_sub_cipher_decrypt import main as multi_decrypt
from sub_cipher_encrypt import main as encrypt

# compare the solution key to the actual key
# generated by the encypting program
def check_key():
    correct_letters = 0

    with open('og-encryption-key.txt', 'r') as f:
        correct_key = f.read().split('\n')

    with open('encrypted-message-key.txt') as f:
        generated_key = f.read().split('\n')

    for i in range(len(correct_key)):
        if correct_key[i] == generated_key[i]:
            correct_letters += 1

    return correct_letters

# run a given program an arbitrary amount of times
# and record their results in a file
def main():
    test_number = int(sys.argv[1])
    use_multiprocessing = sys.argv[2]
    total_time = 0
    total_score = 0

    # use multiprocessing if flag specifies it
    if use_multiprocessing == '-m':
        # clear the previous content of the file
        with open('multi-process-tests.txt', 'w') as f:
            pass

        for i in range(test_number):
            encrypt('message.txt')

            time = multi_decrypt('encrypted-message.txt')
            total_time += time

            score = check_key()
            total_score += score

            with open('multi-process-tests.txt', 'a') as f:
                f.write(f'test {i+1} {time} {score}\n')

            print(f'Test {i+1} has finished.. {i+1}/{test_number} tests left..')

        with open('multi-process-tests.txt', 'a') as f:
            f.write(f'total tests: {test_number}\n')
            f.write(f'average time: {total_time / test_number}\n')
            f.write(f'average score: {total_score / test_number}\n')
    # use no multiprocessing if flag specifies it
    elif use_multiprocessing == '-s':
        # clear the previous content of the file
        with open('single-process-tests.txt', 'w') as f:
            pass

        for i in range(test_number):
            encrypt('message.txt')

            time = single_decrypt('encrypted-message.txt')
            total_time += time

            score = check_key()
            total_score += score

            with open('single-process-tests.txt', 'a') as f:
                f.write(f'test {i+1} {time} {score}\n')

            print(f'Test {i+1} has finished.. {i+1}/{test_number} tests left..')

        with open('single-process-tests.txt', 'a') as f:
            f.write(f'total tests: {test_number}\n')
            f.write(f'average time: {total_time / test_number}\n')
            f.write(f'average score: {total_score / test_number}\n')

if __name__ == '__main__':
    main()