'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

from utils import decorator, word_divider, print_task, results_divider
from initializer import user_initialization, auto_initialization

TASK = '''Task: write a program for processing real lists. The program \
must contain the following basic functions:
            1) input of list elements by the user;
            2) checking the correctness of the entered data;
            3) implementation of the main task with output of results;
            4) displaying the list on the screen.

Option 16 ==> Find the sum of non-negative elements and the product of \
the elements of the list located between the maximum and minimum \
absolute elements.'''

def find_sum_and_product(numbers: list) -> tuple[float, float]:
    """Finds the sum and the product of non-negative numbers between \
the maximum and minimum absolute values in a list.

    Args:
        numbers (list): A list of numbers.

    Returns:
        tuple[float, float]: A tuple containing the sum of positive \
numbers and the product of the numbers between the maximum and minimum \
absolute values.

    """
    max_value = max(numbers, key=abs)
    min_value = min(numbers, key=abs)

    max_index = numbers.index(max_value)
    min_index = numbers.index(min_value)

    start_index = min(max_index, min_index) + 1
    end_index = max(max_index, min_index)

    sum_positive = sum(x for x in numbers[start_index:end_index] if x >= 0)

    product = 1
    for x in numbers[start_index:end_index]:
        product *= x

    return sum_positive, product

@decorator
def main():
    """Run Task 5. Processes input data and outputs the result.

    """
    word_divider('Task 5. Data processing'.upper())
    print_task(TASK)

    numbers = []

    print('Automatically generate list items? [Y/n] ', end='')
    if input().lower() == 'y':
        auto_initialization(numbers)
    else:
        user_initialization(numbers)

    results_divider()

    print('Sequence: ', ', '.join([str(number) for number in numbers]),
          '.', sep='', end='\n\n')

    sum_positive, product = find_sum_and_product(numbers)
    print('Sum of non-negative elements:', sum_positive)
    print('Product of elements:', product)

if __name__=="__main__":
    main()
