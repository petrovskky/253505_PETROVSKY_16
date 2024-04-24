"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import re
import os


class Analyzer:
    """
    A class for analyzing the text content of a file.

    Attributes:
        _input_file (str): The path to the input file.

    Methods:
        input_file (property): Getter and setter for the input file path.
        analyze(): Analyzes the text content of the input file and \
returns various statistics.

    Raises:
        ValueError: If the input file does not exist.

    """
    def __init__(self, input_file):
        """
        Initializes a new instance of the Analyzer class.

        Args:
            input_file (str): The path to the input file.

        """
        self._input_file = input_file

    @property
    def input_file(self):
        """
        Get the file path.

        Returns:
            str: The path to the input file.

        """
        return self._input_file

    @input_file.setter
    def input_file(self, value: str):
        """
        Set the path to the input file.

        Args:
            value (str): The new path to the input file.

        Raises:
            ValueError: If the new file does not exist.

        """
        if os.path.isfile(value):
            self._input_file = value
        else:
            raise ValueError("This file does not exists.")

    def analyze(self):
        """
        Analyze the text content of the input file and return various \
statistics.

        Returns:
            tuple: A tuple containing the following statistics:
                - Total number of sentences
                - Number of narrative sentences
                - Number of interrogative sentences
                - Number of imperative sentences
                - Number of smileys
                - Average sentence length
                - Average word length

        """
        # Read text from file
        cwd = os.getcwd()
        with open(cwd + '\\task2\\' + self.input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        if len(text) == 0 or text == None:
            raise ValueError("Error: empty file.")

        # General task

        # Number of sentences of each type separately
        narrative_count = len(re.findall(r'[A-Za-z][^.!?]*\.', text))
        interrogative_count = len(re.findall(r'[A-Za-z][^.!?]*\?', text))
        imperative_count = len(re.findall(r'[A-Za-z][^.!?]*!', text))

        # Total number of sentences
        sentence_count = narrative_count \
            + interrogative_count \
            + imperative_count

        # Average sentence length
        words = re.findall(r'\b\w+\b', text)
        num_words = len(words)
        total_length = sum(len(word) for word in words)
        avg_sentence_length = total_length / sentence_count

        avg_word_length = total_length / num_words

        num_smileys = re.findall(r'(?<![:;])[;:]-*(?:\[+|\]+|\)+|\(+)', text)

        return sentence_count, narrative_count, interrogative_count, \
            imperative_count, num_smileys, avg_sentence_length, avg_word_length
