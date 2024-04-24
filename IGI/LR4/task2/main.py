"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

from utils.division import print_task, word_divider
from .analyzer import Analyzer
from .special_analyzer import SpecialAnalyzer
import zipfile
import os


TASK = """Task: Create a program for text analysis. Read text from the \
source file. Using regular expressions, obtain the required \
information, display it on the screen and save it to another file. \
Zip the result file using the zipfile module and provide information \
about the file in the archive"""

def main():
    """Run Task 2. Processes the initial data, output of results to \
console, file and zipfile.

    """
    word_divider('Task 2. Text analyzer'.upper())

    print_task(TASK)
    analyzer = Analyzer('test.txt')
    try:
        sentence_count, narrative_count, interrogative_count, imperative_count, \
            smile_count, avg_sentence_length, \
                avg_word_length = analyzer.analyze()
    except ValueError as exc:
        print(exc.args[0])
        return

    analyzer = SpecialAnalyzer('test.txt')
    try:
        replaced_text, time_constructions, max_len_word_count, words_after, \
            max_e_word = analyzer.analyze()
    except ValueError as exc:
        print(exc.args[0])
        return

    # Output results to console
    print('General task')
    print('Number of sentences:', sentence_count)
    print('Number of narrative sentences:', narrative_count)
    print('Number of interrogative sentences:', interrogative_count)
    print('Number of imperative sentences:', imperative_count)
    print('Number of smileys:', smile_count)
    print('Average sentence length:', avg_sentence_length)
    print('Average word length:', avg_word_length)
    print('\nOption 16 task')
    print('Replaced text', replaced_text)
    print('Time constructions:', time_constructions)
    print('Max length word count', max_len_word_count)
    print('Words with "," or "." after:', words_after)
    print('Max length word ends with "e":', max_e_word)

    # Save results to file
    cwd = os.getcwd()
    output_file = cwd + '\\task2\\' + 'results.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        # General task
        file.write('General task\n')
        file.write(f'Number of sentences: {sentence_count}\n')
        file.write(f'Number of narrative sentences: {narrative_count}\n')
        file.write(f'Number of interrogative sentences: \
{interrogative_count}\n')
        file.write(f'Number of imperative sentences: {imperative_count}\n')
        file.write(f'Average sentence length: {avg_sentence_length}\n')
        file.write(f'Average word length: {avg_word_length}\n')
        file.write(f'Number of smileys: {smile_count}\n')
        # Option 16
        file.write('\nOption 16 task\n')
        file.write(f'Replaced text: {replaced_text}\n')
        file.write(f'Time constructions: {time_constructions}\n')
        file.write(f'Max length word count: {max_len_word_count}\n')
        file.write(f'Words with "," or "." after: {words_after}\n')
        file.write(f'Max length word ends with "e": {max_e_word}\n')

    # Archive results file
    cwd = os.getcwd()
    archive_name = cwd + '\\task2\\' + 'results.zip'
    with zipfile.ZipFile(archive_name, 'w') as archive:
        archive.write(output_file)

if __name__ == "__main__":
    main()
