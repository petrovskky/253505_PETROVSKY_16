"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

from .musician import Musician


class MusicExam:
    """
    A class representing a music exam.

    Attributes:
        applicants (dict): A dictionary containing applicant \
information, where the keys are specialties and the values are lists \
of musicians.

    Methods:
        __init__(): Initializes a new instance of the MusicExam class.
        add_applicant(name: str, instrument: str, specialty: str): \
Adds an applicant to the exam.
        get_applicant(name: str) -> tuple[Musician, str]: Retrieves an \
applicant by name.
        get_applicants() -> dict: Returns the dictionary of applicants.

    """
    def __init__(self):
        """
        Initializes a new instance of the MusicExam class.

        """
        self.applicants = {}

    def add_applicant(self, name: str, instrument: str, specialty: str):
        """
        Adds an applicant to the exam.

        Args:
            name (str): The name of the applicant.
            instrument (str): The instrument the applicant plays.
            specialty (str): The specialty of the applicant.

        """
        musician = Musician(name.capitalize(), instrument.capitalize())
        if specialty in self.applicants:
            self.applicants[specialty.capitalize()].append(musician)
        else:
            self.applicants[specialty.capitalize()] = [musician]

    def get_applicant(self, name: str) -> tuple[Musician, str]:
        """
        Retrieves an applicant by name.

        Args:
            name (str): The name of the applicant to retrieve.

        Returns:
            tuple[Musician, str]: A tuple containing the musician and \
their specialty, or None if no matching applicant is found.

        """
        for specialty, musicians in self.applicants.items():
            for musician in musicians:
                if musician.name.lower() == name.lower():
                    return musician, specialty
        return None

    def get_applicants(self):
        """
        Returns the dictionary of applicants.

        Returns:
            dict: A dictionary containing applicant information, where \
the keys are specialties and the values are lists of musicians.

        """
        return self.applicants
