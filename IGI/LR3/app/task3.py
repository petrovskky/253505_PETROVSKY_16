'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

import string
from utils import *

task = '''Task: create a program to analyze text entered from the keyboard.

Option 16 ==> In the string entered from the keyboard, count the number of punctuation marks.'''

def count_punctuation(text):
    '''Counts the number of punctuation characters in the text.'''

    count = 0
    punctuation = string.punctuation  # !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~

    for char in text:
        if char in punctuation:
            count += 1

    return count

@decorator
def main():
    '''Run Task 3. Input of initial data, output of results.'''

    word_divider('Task 3. Counting punctuation marks')
    print_task(task)

    text = input('Enter the string: ')
    
    count = count_punctuation(text)

    results_divider()
    
    print('Number of punctuation marks:', count)


if __name__=="__main__":
    main()
