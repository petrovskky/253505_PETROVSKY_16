"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

def decorator(func):
    """Decorator function that enables the repeated execution \
of a function based on user input.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    """
    def inner(*args, **kwargs):
        """Inner function that wraps the original function and \
handles the repetition.

        Args:
            *args: Positional arguments passed to the original function.
            **kwargs: Keyword arguments passed to the original function.

        Returns:
            The return value of the original function.

        """
        while True:
            result = func(*args, **kwargs)
            print('\nRepeat task? [Y/n] ', end='')
            choice = input().lower()
            if choice != 'y':
                break
        return result

    return inner