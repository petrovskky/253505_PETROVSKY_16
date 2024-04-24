"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

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
    print()
    print(word.center(len(word) + 2).center(DEFAULT_LEN, delimiter))
    print()

def results_divider():
    """Prints a line divider for results using the word_divider \
function.

    """
    word_divider('RESULT', SECONDARY)
