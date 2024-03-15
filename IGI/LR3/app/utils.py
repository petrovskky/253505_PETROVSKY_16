'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

primary = '='
secondary = '-'

default_len = 150

def divider(delimiter=primary):
    print(delimiter * default_len)

def print_task(text):
    print(text)
    word_divider('START', secondary)

def word_divider(word, delimiter=primary):
    len_word = len(word)
    side = delimiter * ((default_len - len_word) // 2 - 1)
    result = side + ' ' + word + ' ' + side
    print()
    print(result if len_word % 2 == 0 else result + delimiter)
    print()

def results_divider():
    word_divider('RESULT', secondary)

def repeat():
    print('\nRepeat task? [Y/n] ', end='')
    if input().lower() == 'y':
        return True
    else:
        return False
    
def decorator(func):
    def inner(*args, **kwargs):
        while True:
            result = func(*args, **kwargs)
            print('\nRepeat task? [Y/n] ', end='')
            choice = input().lower()
            if choice != 'y':
                break
        return result
        
    return inner
