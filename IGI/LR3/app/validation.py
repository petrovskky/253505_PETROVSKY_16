'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

def int_validation(string: str) -> bool:
    """Validates and converts a string to an integer.

    Args:
        string (str): The input string to be validated and converted.

    Returns:
        int: The converted integer value.

    Raises:
        ValueError: If the string cannot be converted to an integer.

    """
    try:
        n = int(string)
        return n
    except ValueError as exc:
        raise ValueError('Enter int value') from exc

def float_validation(string: str) -> bool:
    """Validates and converts a string to a float.

    Args:
        string (str): The input string to be validated and converted.

    Returns:
        float: The converted float value.

    Raises:
        ValueError: If the string cannot be converted to a float.

    """
    try:
        n = float(string)
        return n
    except ValueError as exc:
        raise ValueError('Enter float value') from exc
