'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

import random
from validation import *

def get_size():
    while True:
        print('Enter the number of list items: ', end='')

        try:
            size = int_validation(input())
        except ValueError:
            print('Error: enter integer value.')
            continue
        except Exception:
            print('Fail input. Try again.')
            continue

        if (size < 1):
            print('Error: the number of elements must be a positive number.')
            continue

        break

    return size

def user_initialization(sequence):
    '''Provides user input for list items.'''

    n = get_size()

    for i in range(n):
        while True:
            print(f'Enter a list item # {i+1}: ', end='')
            try:
                num = float_validation(input())
            except ValueError:
                print('Error: enter float value.')
                continue
            except Exception:
                print('Fail input. Try again.')
                continue
            break

        sequence.append(num)
    
    return sequence

def auto_initialization(sequence):
    n = get_size()

    for _ in range(n):
        sequence.append(random.uniform(-100, 100))

    return sequence
