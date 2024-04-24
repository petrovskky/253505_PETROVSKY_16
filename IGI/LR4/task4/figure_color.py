"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

class FigureColor:
    """
    A class representing the color of a geometric figure.

    Attributes:
        _color (str): The color of the figure.

    Methods:
        color (property): Getter and setter for the color of the figure.

    """
    def __init__(self, color=None):
        """
        Constructor for the FigureColor class.

        Args:
            color (str, optional): The color of the figure. Defaults \
to None.

        """
        self._color = color

    @property
    def color(self):
        """Getter method for the color property.

        Returns:
            str: The color of the figure.

        """
        return self._color

    @color.setter
    def color(self, value):
        """Setter method for the color property.

        Args:
            value (str): The new color for the figure.

        """
        self._color = value
