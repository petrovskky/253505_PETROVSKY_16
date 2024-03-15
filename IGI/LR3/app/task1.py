'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

from math import sin as sin
from math import pi as Pi
from utils import *
from validation import *

task = '''Task: create a program to calculate the value of a function using a power series \
expansion of the function. Set the precision of calculations eps. \
Provide a maximum number of iterations equal to 500. \
Print the number of series terms required to achieve the specified calculation accuracy.

Option 16 ==> F(x) = sin(x)'''

def factorial(n):
    '''Calculate factorial of a number.'''
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def sin_taylor(x, eps):
    '''Calculate sin(x) using Taylor series approximation.'''

    result = 0
    sign = 1
    temp = x
    n = 0

    while abs(temp) >= eps:
        result += temp
        n += 1
        sign *= -1
        temp = sign * (x ** (2 * n + 1)) / factorial(2 * n + 1)        
        
        if n > 500:  # Maximum number of iterations
            break

    return result, n

@decorator
def main():
    '''Run Task 1. Input of initial data, their processing, output of results.'''

    word_divider('Task 1. Calculating the sin(x) function'.upper())
    print_task(task)

    while True:
        print('Enter the value of x in rad: ', end='')

        try:
            x = float_validation(input())
        except ValueError:
            print('Error: enter float value.')
            continue
        except Exception:
            print('Fail input. Try again.')
            continue

        if (x > 10000000000):
            print('The value is too big. Enter number in range 1e10.')
            continue

        break

    while True:
        print('Enter the desired precision (epsilon): ', end='')
        try:
            eps = float_validation(input())
        except ValueError:
            print('Error: enter float value.')
            continue
        except Exception:
            print('Fail input. Try again.')
            continue

        if (eps == 0):
            print('Error: the value of epsilon cannot be zero.')
            continue
        break

    results_divider()

    orig_x = x

    x %= 2 * Pi

    result, n = sin_taylor(x, eps)
    math_result = sin(orig_x)

    print(f'x\t\t\tn\t\tF(x)\t\t\t\tMath F(x)\t\t\teps\n{str(orig_x).ljust(18, " ")}\t{n}\t\t{result:.16f}'
            + f'\t\t{math_result:.16f}\t\t{eps}')


if __name__=="__main__":
    main()
