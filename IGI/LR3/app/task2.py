'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

from utils import *
from validation import *

task = '''Task: create a loop that takes integers and calculates the number of even natural numbers. End - enter 0.

Option 16 ==> Calculates the number of even natural numbers.'''

def is_corresponds(n):
    '''Determines whether the number meets the requirements of the task or not.'''

    return n > 0 and n % 2 == 0

@decorator
def main():
    '''Run Task 2. Input of initial data, their processing, output of results.'''

    word_divider('Task 2. Counting even natural numbers'.upper())
    print_task(task)

    count = 0

    while True:
        while True:
            print('Enter an integer (enter 0 to exit): ', end='')
            try:
                num = int_validation(input())
            except ValueError:
                print('Error: enter integer value.')
                continue
            except Exception:
                print('Fail input. Try again.')
                continue
            break

        if num == 0:
            break
        
        if is_corresponds(num):
            count += 1
            
    results_divider()
    print('Count of even natural numbers:', count)


if __name__=="__main__":
    main()
    