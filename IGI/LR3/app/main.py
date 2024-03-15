'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

import task1, task2, task3, task4, task5
from utils import *
from validation import *

tasks = {
    1: task1.main,
    2: task2.main,
    3: task3.main,
    4: task4.main,
    5: task5.main
}

def main():
    '''Runs a task of the user's choosing.'''

    while True:
        word_divider('Menu'.upper())

        while True:
            try:
                print('Enter number to run task (1 - 5) or 0 to exit: ', end='')
                choice = int_validation(input())
            except ValueError:
                print('Error: enter int value.')
                continue
            except Exception:
                print('Fail input. Try again.')
                continue

            if choice not in tasks and choice != 0:
                print('Error: there is no task with this number.')
                continue

            break
        
        if choice == 0:
            break

        tasks[choice]()


if __name__=="__main__":
    main()
