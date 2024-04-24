"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import sys
sys.path.append("..")
from utils.division import word_divider, print_task
from utils.repeater import decorator
from .validation import radius_validation, check_color_exists
from .circle import Circle
from .builder import Builder


TASK = """Task: Develop base classes and descendant classes on the topic \
“geometric shapes”.

The program must contain the following basic functions:
    1) input of parameter values by the user;
    2) checking the correctness of the entered data;
    3) constructing, painting the figure in the selected color entered \
from the keyboard, and signing the figure with text entered from the \
keyboard;
    4) output the figure to the screen and to a file.

Option 16 ==> Construct a triangle circumscribed about a circle with \
radius R."""

@decorator
def main():
    """Run Task 4. Input of initial data, output of results.

    """
    word_divider('Task 4. Triangle and circle'.upper())
    print_task(TASK)

    while True:
        print('Enter radius: ', end='')

        try:
            r = radius_validation(input())
        except ValueError as exc:
            print(exc.args[0])
            continue

        break

    circle = Circle(r)

    print(circle.get_info())

    while True:
        print('Enter circle color: ', end='')

        try:
            color = check_color_exists(input())
        except ValueError:
            print('Error: no such a color. Try again.')
            continue

        break

    circle.color = color

    Builder.build_and_save(radius=r, color=circle.color,
                           title='Triangle and inscribed circle')

if __name__=="__main__":
    main()
