"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import sys
sys.path.append("..")
from utils.validator import float_validation
import matplotlib.colors as mcolors


def radius_validation(string: str) -> bool:
    """
    Validates and returns the valid radius value.

    Args:
        string (str): String representation of the radius.

    Returns:
        float: The valid radius value.

    Raises:
        ValueError: If the input string cannot be converted to a float \
or if the radius is less than or equal to 0.

    """
    try:
        n = float_validation(string)
    except ValueError:
        raise ValueError('Error: enter float value.')

    if n <= 0:
        raise ValueError('Error: assigning a radius a non-positive number.')

    return n

def check_color_exists(color):
    """
    Checks if the given color is a valid Matplotlib color.

    Args:
        color: The color to be checked.

    Returns:
        tuple: The RGB tuple representation of the color.

    Raises:
        ValueError: If the given color is not a valid Matplotlib color.

    """
    try:
        clr = mcolors.to_rgb(color)
        return clr
    except ValueError:
        raise
