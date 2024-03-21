'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

PRIMARY = '='
SECONDARY = '-'

DEFAULT_LEN = 150

def divider(delimiter=PRIMARY):
    """Prints a divider line consisting of a repeated delimiter \
character.

    Args:
        delimiter (str): The character used as the delimiter. \
Defaults to the value of PRIMARY.

    """
    print(delimiter * DEFAULT_LEN)

def print_task(text: str):
    """Prints a given text and calls the word_divider function.

    Args:
        text (str): The text to be printed.

    """
    print(text)
    word_divider('START', SECONDARY)

def word_divider(word, delimiter=PRIMARY):
    """Prints a line with a word surrounded by delimiters.

    Args:
        word (str): The word to be surrounded by delimiters.
        delimiter (str): The character used as the delimiter. \
Defaults to the value of PRIMARY.

    """
    len_word = len(word)
    side = delimiter * ((DEFAULT_LEN - len_word) // 2 - 1)
    result = side + ' ' + word + ' ' + side
    print()
    print(result if len_word % 2 == 0 else result + delimiter)
    print()

def results_divider():
    """Prints a line divider for results using the word_divider \
function.

    """
    word_divider('RESULT', SECONDARY)

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
