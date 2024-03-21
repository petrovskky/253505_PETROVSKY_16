'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

from math import sin as Sin
from math import pi as Pi
from utils import decorator, word_divider, print_task, results_divider
from validation import float_validation

TASK = '''Task: create a program to calculate the value of a function \
using a power series expansion of the function. Set the precision of \
calculations eps. Provide a maximum number of iterations equal to 500. \
Print the number of series terms required to achieve the specified \
calculation accuracy.

Option 16 ==> F(x) = sin(x)'''

MAX_ITERATION = 500

MAX_VALUE = 1e10

def factorial(n: int) -> int:
    """Calculates the factorial of a number.

    Args:
        n (int): The number for which to calculate the factorial.

    Returns:
        int: The factorial of the input number.

    """
    if n == 0:
        return 1
    return n * factorial(n - 1)

def sin_taylor(x: float, eps: float ) -> tuple[float, int]:
    """Calculates an approximation of the sine function using the \
Taylor series expansion.

    Args:
        x (float): The input value for which to calculate the sine.
        eps (float): The desired accuracy of the approximation.

    Returns:
        tuple[float, int]: A tuple containing the approximation of \
sine and the number of iterations performed.

    """
    result = 0
    sign = 1
    temp = x
    n = 0

    while abs(temp) >= eps:
        result += temp
        n += 1
        sign *= -1
        temp = sign * (x ** (2 * n + 1)) / factorial(2 * n + 1)

        if n > MAX_ITERATION:
            break

    return result, n

@decorator
def main():
    """Run Task 1. Input of initial data, \
their processing, output of results.

    """
    word_divider('Task 1. Calculating the sin(x) function'.upper())
    print_task(TASK)

    while True:
        print('Enter the value of x in rad: ', end='')

        try:
            x = float_validation(input())
        except ValueError:
            print('Error: enter float value.')
            continue

        if x > MAX_VALUE:
            print(f'The value is too big. Enter number in range {MAX_VALUE}.')
            continue

        break

    while True:
        print('Enter the desired precision (epsilon): ', end='')
        try:
            eps = float_validation(input())
        except ValueError:
            print('Error: enter float value.')
            continue

        if eps == 0:
            print('Error: the value of epsilon cannot be zero.')
            continue

        break

    results_divider()

    orig_x = x

    x %= 2 * Pi

    result, n = sin_taylor(x, eps)
    math_result = Sin(orig_x)

    print('x\t\t\tn\t\tF(x)\t\t\t\tMath F(x)\t\t\teps\n'
          + f'{str(orig_x).ljust(18, " ")}\t{n}\t\t{result:.16f}'
            + f'\t\t{math_result:.16f}\t\t{eps}')

if __name__=="__main__":
    main()
