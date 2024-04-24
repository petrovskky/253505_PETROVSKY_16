"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import sys
sys.path.append("..")
from utils.division import print_task, results_divider, word_divider
from utils.validator import float_validation
from utils.repeater import decorator
from .sequence_analyzer import SequenceAnalyzer
from .builder import Builder
import numpy as np


TASK = """Task: Modify the program from LR3 using the class.

Build and save graphs:
    - a graph based on the obtained data of series expansion \
of a function, presented in the table,
    - graph of the corresponding function represented using \
the math module

Option 16 ==> F(x) = sin(x)"""

MAX_VALUE = 1e10

@decorator
def main():
    """Run Task 3. Input of initial data, output of results..

    """
    word_divider('Task 3. Function graphs'.upper())
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

    analyzer = SequenceAnalyzer(x, eps)
    result, n = analyzer.sin_taylor()
    math_result = np.sin(x)

    print('x\t\t\tn\t\tF(x)\t\t\t\tMath F(x)\t\t\teps\n'
          + f'{str(x):18}\t{n}\t\t{result:.16f}'
            + f'\t\t{math_result:.16f}\t\t{eps}')
    print(
        '\nArithmetic mean of sequence elements:',
        analyzer.calculate_average()
    )
    print('Median:', analyzer.calculate_median())
    print('Mode:', analyzer.calculate_mode())
    print('Variance:', analyzer.calculate_variance())
    print(
        'Sequence standard deviation:',
        analyzer.calculate_standard_deviation()
    )

    input('\nPress any key to build graphs...')

    x = np.linspace(0, 20, 100)
    y1 = np.sin(x)
    y2 = [SequenceAnalyzer(x, 1e-10).sin_taylor()[0] for x in x]

    Builder.build_and_save(x=x, y1=y1, y2=y2, label_y1='MathSin(x)', \
                          label_y2='Sin(x)', annotation='local max', \
                            xy_annotation=(5 * np.pi / 2, 1), \
                                xytext_annotation=(9.5, 1.5))

if __name__=="__main__":
    main()
