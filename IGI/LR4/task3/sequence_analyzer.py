"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

from math import pi as Pi
from statistics import median, mean, mode, variance, stdev


class SequenceAnalyzer:
    """
    A class for analyzing a sequence of numbers.

    Attributes:
        _x (float): The input value x.
        _eps (float): The desired accuracy.
        _sequence (list): The sequence of numbers.

    Methods:
        x (property): Getter and setter for the x value.
        sequence (property): Getter for the sequence list.
        sin_taylor(): Calculates an approximation of the sine function \
using the Taylor series expansion.
        calculate_average(): Calculates the average of the sequence.
        calculate_median(): Calculates the median of the sequence.
        calculate_mode(): Calculates the mode of the sequence.
        calculate_variance(): Calculates the variance of the sequence.
        calculate_standard_deviation(): Calculates the standard \
deviation of the sequence.

    """
    def __init__(self, x: float, eps: float):
        """Constructor for the SequenceAnalyzer class.

        Initializes an instance of the class with the given values \
x and eps, and calls the sin_taylor() method to compute the sequence \
using the Taylor series expansion.

        Args:
            x (float): The input value x.
            eps (float): The desired accuracy.

        """
        self._x = x
        self._eps = eps
        self._sequence = []
        self.sin_taylor()

    @property
    def x(self):
        """Getter method for the x property.

        Returns:
            float: The value of x.

        """
        return self._x

    @x.setter
    def x(self, value: float):
        """Setter method for the x property.

        Args:
            value (float): The new value for x.

        Raises:
            TypeError: If the value is not a float.

        """
        if (isinstance(value, float)):
            self._x = value
        else:
            raise TypeError("Invalid name. It must be a float.")

    @property
    def sequence(self):
        """Getter method for the sequence property.

        Returns:
            list: The sequence list.

        """
        return self._sequence

    def sin_taylor(self) -> tuple[float, int]:
        """Calculates an approximation of the sine function using the \
Taylor series expansion.

        Args:
            x (float): The input value for which to calculate the sine.
            eps (float): The desired accuracy of the approximation.

        Returns:
            tuple[float, int]: A tuple containing the approximation of \
sine and the number of iterations performed.

        """
        def factorial(n: int) -> int:
            """Calculates the factorial of a number.

            Args:
                n (int): The number to calculate the factorial.

            Returns:
                int: The factorial of the input number.

            """
            if n == 0:
                return 1
            return n * factorial(n - 1)

        MAX_ITERATION = 500

        result = 0
        sign = 1
        temp_x = self.x % (2 * Pi)
        temp = temp_x
        n = 0

        while abs(temp) >= self._eps:
            self._sequence.append(temp)
            result += temp
            n += 1
            sign *= -1
            temp = sign * (temp_x ** (2 * n + 1)) / factorial(2 * n + 1)

            if n > MAX_ITERATION:
                break

        return result, n

    def calculate_average(self):
        """Calculates the average of the sequence using statistics lib.

        Returns:
            float: The average value.

        """
        return mean(self.sequence)

    def calculate_median(self):
        """Calculates the median of the sequence using statistics lib.

        Returns:
            float: The median value.

        """
        return median(self.sequence)

    def calculate_mode(self):
        """Calculates the mode of the sequence using statistics lib.

        Returns:
            Any: The mode value.

        """
        return mode(self.sequence)

    def calculate_variance(self):
        """Calculates the variance of the sequence using statistics lib.

        Returns:
            float: The variance value.

        """
        return variance(self.sequence)

    def calculate_standard_deviation(self):
        """Calculates the standard deviation of the sequence using \
statistics lib.

        Returns:
            float: The standard deviation value.

        """
        return stdev(self.sequence)
