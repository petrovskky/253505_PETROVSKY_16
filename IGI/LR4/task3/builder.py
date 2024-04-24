"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import matplotlib.pyplot as plt
from numpy import pi as Pi
import os


class Builder:
    @staticmethod
    def build_and_save(x=[], y1=[], y2=[], label_y1=None, label_y2=None, \
             annotation=None, xy_annotation=None, xytext_annotation=None):
        """Builds a graph with two plots and saves it as an image.

        Args:
            x (array-like): The x-values for the plots.
            y1 (array-like): The y-values for the first plot.
            y2 (array-like): The y-values for the second plot.
            label_y1 (str): The label for the first plot.
            label_y2 (str): The label for the second plot.
            annotation (str): The annotation text.
            xy_annotation (tuple): The coordinates of the \
annotation (x, y).
            xytext_annotation (tuple): The coordinates of the text \
offset (x, y).

        Returns:
            None

        """
        plt.plot(x, y1, color='blue', linestyle='-', \
                 linewidth=3, label=label_y1)
        plt.plot(x, y2, color='red', linestyle=' ', \
                 linewidth=1, marker='o', markersize=3, label=label_y2)

        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)

        plt.legend()

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Graphs of {label_y1} and {label_y2} functions')

        plt.xlim(min(x), max(x))
        plt.ylim(min(min(y1), min(y2)) * 2, max(max(y1), max(y2)) * 2)

        if not any(obj is None for obj in (
            annotation,
            xy_annotation,
            xytext_annotation
        )):
            plt.annotate(annotation, xy=xy_annotation, \
                         xytext=xytext_annotation,
                arrowprops=dict(facecolor='black', shrink=0.05))

        cwd = os.getcwd()
        plt.savefig(cwd + '\\task3\\' + 'plot.png')

        plt.show()
