'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

import task1
import task2
import task3
import task4
import task5
from utils import word_divider
from validation import int_validation

tasks = {
    1: task1.main,
    2: task2.main,
    3: task3.main,
    4: task4.main,
    5: task5.main
}

def main():
    """Runs a task of the user's choosing.

    """
    while True:
        word_divider('Menu'.upper())

        while True:
            try:
                print('Enter number to run task (1 - 5) or 0 to exit: ',
                      end='')
                choice = int_validation(input())
            except ValueError:
                print('Error: enter int value.')
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
