'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

def int_validation(input):
    '''Checks if the input value is an integer.'''

    try:
        n = int(input)
        return n
    except ValueError:
        raise ValueError('Enter int value')
    
def float_validation(input):
    '''Checks if the input value is a floating-point number.'''

    try:
        n = float(input)
        return n
    except ValueError:
        raise ValueError('Enter float value')
    