"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import sys
sys.path.append("..")
from utils.division import print_task, word_divider, results_divider
from .music_exam import MusicExam
from .music_exam_serializer import MusicExamSerializer
from .initialization import applicants


TASK = """Task: The source data is a dictionary. You need to put them into a \
file using a serializer. Organize data reading, searching, sorting in \
accordance with the individual task. Be sure to use classes. Implement \
two options:
    1) CSV file format;
    2) pickle module."""

def input_musician():
    """
    Prompt the user to input musician details.

    Returns:
        tuple[str, str, str]: A tuple containing the name, instrument, \
and specialty entered by the user.

    """
    while True:
        try:
            name = input('Enter musician name:')
            if not name.isalpha():
                raise TypeError
            break
        except TypeError:
            print('Error: enter correct name.\n')
    while True:
        try:
            instrument = input('Enter instrument:')
            if not instrument.isalpha():
                raise TypeError
            break
        except TypeError:
            print('Error: enter correct instrument.\n')
    while True:
        try:
            specialty = input('Enter specialty:')
            if not specialty.isalpha():
                raise TypeError
            break
        except TypeError:
            print('Error: enter correct specialty.\n')

    return name, instrument, specialty

def main():
    """Run Task 1. Processes the initial data, output of results.

    """
    word_divider('Task 1. Serializer'.upper())

    print_task(TASK)

    MusicExamSerializer.serialize_dict_to_csv(applicants, 'applicants.csv')

    exam_csv = MusicExamSerializer.deserialize_csv('applicants.csv')

    MusicExamSerializer.serialize_pkl(exam_csv, 'applicants.pkl')
    exam_pkl = MusicExamSerializer.deserialize_pkl('applicants.pkl')

    while True:
        print('Enter musician name to get info (enter 0 to exit / 1 to \
add): ', end='')
        name = input()

        if name == '0':
            break

        if name == '1':
            n, i, s = input_musician()
            exam_pkl.add_applicant(name=n, instrument=i, specialty=s)
            continue

        applicant = exam_pkl.get_applicant(name)

        if applicant:
            print(f'\nName: {applicant[0].name}\tInstrument: \
{applicant[0].instrument}\tSpecialty: {applicant[1]}\n')
        else:
            print('No musician with this name\n')


if __name__ == "__main__":
    main()
