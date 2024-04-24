"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

from abc import ABC, abstractmethod


class GeometricFigure(ABC):
    """
    An abstract base class that represents a geometric figure.

    This class defines the basic structure and behavior of a geometric \
figure, including the requirement to implement the `calculate_area()` \
method.

    Subclasses of `GeometricFigure` must implement the \
`calculate_area()` method to provide the specific logic for \
calculating the area of that geometric figure.

    """
    @abstractmethod
    def calculate_area(self):
        """
        Calculates and returns the area of the geometric figure.

        Returns:
            float: The area of the geometric figure.

        """
        pass
