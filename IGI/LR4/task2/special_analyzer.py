"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import re
import os
from .analyzer import Analyzer


class SpecialAnalyzer(Analyzer):
    """
    A subclass of the 'Analyzer' class that performs additional text \
analysis tasks.

    Inherits the 'input_file' property and `analyze()` method from the \
'Analyzer' class.

    Methods:
        analyze(): Performs additional text analysis tasks on the \
input file and returns the results.

    """
    def __init__(self, input_file):
        """
        Initializes the 'SpecialAnalyzer' object.

        Args:
            input_file (str): The path to the input file.

        """
        super().__init__(input_file)

    def analyze(self):
        """
        Analyzes the text content of the input file and returns the \
results of the additional analysis tasks.

        Returns:
            tuple: A tuple containing the following analysis results:
                - replaced_text (str): The text with the last three \
characters of 5-letter words replaced with '$'.
                - time_constructions (list): A list of time \
constructions (in the format "HH:MM") found in the text.
                - max_len_word_count (int): The count of the longest \
words in the text.
                - words_after (list): A list of words that have a ',' \
or '.' after them.
                - max_e_word (str): The longest word in the text that \
ends with the letter 'e'.

        """
        # Read text from file
        cwd = os.getcwd()
        with open(cwd + '\\task2\\' + self.input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Option 16

        # Replaces the last three characters of words of the selected length
        # with the '$' character
        replaced_text = re.sub(r'\b\w{5}\b',
                               lambda match: match.group()[:-3] + '$', text)

        # Time
        time_pattern = r"\b\d{2}:\d{2}\b"
        time_constructions = re.findall(time_pattern, text)

        # Max length word count
        words = re.findall(r'\b\w+\b', text)
        word_lengths  = [len(word) for word in words]
        max_len_word_count = word_lengths.count(max(word_lengths))

        # Words with ',' or '.' after
        matches = re.findall(r'\b\w+[,\.]', text)
        words_after = [match[:-1] for match in matches]

        # Max length word ends with 'e'
        max_e_word = max([word for word in words if word.endswith('e')],
                         key=lambda word: len(word))

        return replaced_text, time_constructions, max_len_word_count, \
            words_after, max_e_word
