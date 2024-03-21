'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

import random
import validation

def get_size() -> int:
    """Prompts the user to enter the number of list items and returns \
the validated size.

    Returns:
        int: The validated size of the list.

    """
    while True:
        print('Enter the number of list items: ', end='')

        try:
            size = validation.int_validation(input())
        except ValueError:
            print('Error: enter integer value.')
            continue

        if size < 1:
            print('Error: the number of elements must be a positive number.')
            continue

        break

    return size

def user_initialization(sequence: list) -> list:
    """Allows the user to initialize a list by entering values.

    Args:
        sequence (list): The initial list.

    Returns:
        list: The updated list after user initialization.

    """
    n = get_size()

    for i in range(n):
        while True:
            print(f'Enter a list item # {i+1}: ', end='')
            try:
                num = validation.float_validation(input())
            except ValueError:
                print('Error: enter float value.')
                continue
            break

        sequence.append(num)

    return sequence

def auto_initialization(sequence: list) -> list:
    """Automatically initializes a list by generating random float \
values within a range.

    Args:
        sequence (list): The initial list.

    Returns:
        list: The updated list after automatic initialization.

    """
    n = get_size()

    for _ in range(n):
        sequence.append(random.uniform(-100, 100))

    return sequence
