"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import matplotlib.pyplot as plt
from numpy import sqrt
import os


class Builder:
    """
    A class for building and saving plots.

    Methods:
        build_and_save(radius, color, title): Builds and saves a plot \
of a triangle and a circle.

    """
    @staticmethod
    def build_and_save(radius, color, title):
        """
        Builds and saves a plot of a triangle and a circle.

        Args:
            radius (float): The radius of the circle.
            color (str): The color of the circle.
            title (str): The title of the plot.

        """
        side = 2 * radius * sqrt(3)
        # Вычисление координат вершин треугольника
        x = [0, side / 2, side]
        y = [0, sqrt(3) * side / 2, 0]

        # Построение треугольника
        plt.figure()
        plt.plot(x + [x[0]], y + [y[0]], 'b-')

        # Построение окружности
        circle_plt = plt.Circle((side / 2, radius), radius, color=color)
        plt.gca().add_patch(circle_plt)

        plt.axis('equal')  # Одинаковый масштаб по осям x и y
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(title)
        plt.grid(True)

        cwd = os.getcwd()
        plt.savefig(cwd + '\\task4\\' + 'plot.png')

        plt.show()
