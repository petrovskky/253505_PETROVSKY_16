"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import numpy as np


class MatrixOperations:
    """
    A class for performing various operations on a matrix.

    Args:
        matrix (array-like): A 2D array representing the input matrix.

    """
    def __init__(self, matrix):
        """
        Constructor for the MatrixOperations class.

        Args:
            matrix (array-like): A 2D array representing the input \
matrix.

        """
        self._matrix = np.array(matrix)

    def find_column_with_min_sum(self):
        """
        Finds the index of the column in the matrix with the minimum \
sum of its elements.

        Returns:
            int: The index of the column with the minimum sum.

        """
        column_index = np.argmin(np.sum(self._matrix, axis=0))
        return column_index

    def calculate_median_standard(self, column_index):
        """
        Calculates the median of the values in the specified column of \
the matrix
        using the standard `np.median()` function.

        Args:
            column_index (int): The index of the column for which the \
median is to be calculated.

        Returns:
            float: The median value of the specified column.

        """
        median_standard = np.median(self._matrix[:, column_index])
        return median_standard

    def calculate_median_formula(self, column_index):
        """
        Calculates the median of the values in the specified column of \
the matrix by manually implementing the median formula.

        Args:
            column_index (int): The index of the column for which the \
median is to be calculated.

        Returns:
            float: The median value of the specified column.

        """
        column = self._matrix[:, column_index]
        sorted_column = sorted(column)
        n = len(sorted_column)

        if n % 2 == 0:
            mid = n // 2
            median = (sorted_column[mid - 1] + sorted_column[mid]) / 2
        else:
            mid = n // 2
            median = sorted_column[mid]

        return median

    def mean(self, axis=None):
        """
        Calculates the mean of the matrix along the specified axis.

        Args:
            axis (int, optional): The axis along which the mean is calculated.
                If `None`, the mean of the entire matrix is returned.

        Returns:
            float or numpy.ndarray: The mean value(s).

        """
        return np.mean(self._matrix, axis=axis)

    def corrcoef(self):
        """
        Calculates the correlation coefficient matrix of the matrix.

        Returns:
            numpy.ndarray: The correlation coefficient matrix.

        """
        return np.corrcoef(self._matrix.T)

    def var(self, axis=None):
        """
        Calculates the variance of the matrix along the specified axis.

        Args:
            axis (int, optional): The axis along which the variance is calculated.
                If `None`, the variance of the entire matrix is returned.

        Returns:
            float or numpy.ndarray: The variance value(s).

        """
        return np.var(self._matrix, axis=axis)

    def std(self, axis=None):
        """
        Calculates the standard deviation of the matrix along the specified axis.

        Args:
            axis (int, optional): The axis along which the standard deviation is calculated.
                If `None`, the standard deviation of the entire matrix is returned.

        Returns:
            float or numpy.ndarray: The standard deviation value(s).
        """
        return np.std(self._matrix, axis=axis)
