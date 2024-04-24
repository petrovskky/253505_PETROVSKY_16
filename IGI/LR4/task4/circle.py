"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

from .geometric_figure import GeometricFigure
from .figure_color import FigureColor
from numpy import pi


class Circle(GeometricFigure):
    """
    A class representing a circle.

    Attributes:
        _r (float): The radius of the circle.
        _figure_color (FigureColor): The color of the circle.

    Methods:
        color (property): Getter and setter for the color of the circle.
        get_name(): Returns the name of the class.
        calculate_area(): Calculates the area of the circle.
        get_info(): Returns information about the circle.

    """
    def __init__(self, r):
        """
        Constructor for the Circle class.

        Args:
            r (float): The radius of the circle.

        """
        self._r = r
        self._figure_color = FigureColor()

    @property
    def color(self):
        """Getter method for the color property.

        Returns:
            str: The color of the circle.

        """
        return self._figure_color.color

    @color.setter
    def color(self, value):
        """Setter method for the color property.

        Args:
            value (str): The new color for the circle.

        """
        self._figure_color.color = value

    @classmethod
    def get_name(cls):
        """Class method to get the name of the class.

        Returns:
            str: The name of the class.

        """
        return cls.__name__

    def calculate_area(self):
        """Calculates the area of the circle.

        Returns:
            float: The area of the circle.

        """
        return pi * self._r ** 2

    def get_info(self):
        """Gets information about the circle.

        Returns:
            str: Information about the circle.

        """
        return "{} with radius = {}, {} color and area = {}.".format(
    self.get_name(), self._r, self.color, self.calculate_area()
    )
