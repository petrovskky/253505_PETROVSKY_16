'''
Lab: 3
Version: 1.0.0
Author: Petrovsky, 253505
Date: 01.03.2024
'''

from utils import decorator, word_divider, print_task, results_divider

TASK = '''Task: write a program to analyze a string initialized in the \
program code.

Option 16 ==>   a) determine the number of words ending with \
a consonant;
                b) find the average length of words in a line, \
rounding the result to integer, and print all words that have \
that length, or the message “There are no words of length n \
characters in the line”;
                c) print every seventh word'''

STR = '''So she was considering in her own mind, as well as she \
could, for the hot day made her feel very sleepy and stupid, whether \
the pleasure of making a daisy-chain would be worth the trouble of \
getting up and picking the daisies, when suddenly a White Rabbit \
with pink eyes ran close by her.'''

def count_consonant_words(words: list) -> int:
    """Counts the number of words in a list ending with a consonant.

    Args:
        words (list): A list of words to count.

    Returns:
        int: The total count of words ending with a consonant.

    """
    consonant_count = 0
    consonants = "bcdfghjklmnpqrstvwxyz"

    for word in words:
        if word[-1] in consonants:
            consonant_count += 1

    return consonant_count

def average_length_words(words: list) -> tuple[int, list]:
    """Calculates the average length of words in a list and returns \
words with that length.

    Args:
        words (list): A list of words.

    Returns:
        tuple[int, list]: A tuple containing the average length and \
a list of words with that length.

    """
    lengths = [len(word) for word in words]

    if len(lengths) == 0:
        return 0, []

    average_length = round(sum(lengths) / len(lengths))
    words_with_avg_length = [
        word for word in words if len(word) == average_length
    ]

    return average_length, words_with_avg_length

@decorator
def main():
    """Run Task 4. Processes the source data and outputs the result.

    """
    word_divider('Task 4. String parsing'.upper())
    print_task(TASK)

    print('Default string:', STR)

    words = STR.replace(',', '').replace('.', '').lower().split()

    results_divider()

    print(
        'Number of words ending with a consonant:',
        count_consonant_words(words)
    )

    avg_len, avg_list = average_length_words(words)

    print('Average word length:', avg_len)

    if len(avg_list) != 0:
        print(f'Words of length {avg_len}: ', ', '.join(avg_list), '.', sep='')
    else:
        print('There are no words of length n characters in the line')

    seventh_words = words[6::7]  # Finding every seventh word using a slice.

    print('Every seventh word: ', ', '.join(seventh_words), '.', sep='')

if __name__=="__main__":
    main()
