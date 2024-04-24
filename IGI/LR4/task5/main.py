"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import sys
sys.path.append("..")
from utils.division import print_task, results_divider, word_divider
from utils.repeater import decorator
from .initializer import auto_initialization
from .matrix_operations import MatrixOperations


TASK = """Task: Explore the capabilities of the NumPy library when working \
with arrays and mathematical and static operations. Generate an \
integer matrix A[n,m] using a random number generator.

Option 16 ==> Find the column with the smallest sum of elements.
Calculate the median value of this column."""

@decorator
def main():
    """Run Task 5. Generate data, processes and outputs the result.

    """
    word_divider('Task 5. Arrays'.upper())
    print_task(TASK)

    matrix = []

    auto_initialization(matrix)

    results_divider()

    m = MatrixOperations(matrix)

    print('Column index with minimum sum:', m.find_column_with_min_sum())
    print('Median of this column (NumPy):',
          m.calculate_median_standard(m.find_column_with_min_sum()))
    print('Median of this column:',
          m.calculate_median_formula(m.find_column_with_min_sum()))
    print('The correlation coefficient:\n', m.corrcoef())
    print('The mean of the matrix:', m.mean())
    print('The standard deviation of the matrix:', m.std())

if __name__=="__main__":
    main()
