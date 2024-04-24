"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import sys
sys.path.append("..")
from utils.validator import int_validation
import random

def get_size(name) -> int:
    """Prompts the user to enter the number columns or rows.

    Returns:
        int: The validated size of the column or row.

    """
    while True:
        print(f'Enter the number of {name}: ', end='')

        try:
            size = int_validation(input())
        except ValueError:
            print('Error: enter integer value.')
            continue

        if size < 1:
            print('Error: the number of elements must be a positive number.')
            continue

        break

    return size

def generate_sequence(n: int):
    """
    Generates a sequence of random numbers in the range from -100 to 100.

    Args:
    - n (int): The desired length of the sequence.

    Returns:
    - A generator that yields a random number at each iteration.

    """
    for _ in range(n):
        yield random.uniform(-100, 100)

def auto_initialization(sequence: list) -> list:
    """Automatically initializes a list by using generate_sequence.

    Args:
        sequence (list): The initial list.

    Returns:
        list: The updated list after automatic initialization.

    """
    n = get_size('row')
    m = get_size('col')

    for _ in range(n):
        sequence.append([e for e in generate_sequence(m)])

    return sequence
