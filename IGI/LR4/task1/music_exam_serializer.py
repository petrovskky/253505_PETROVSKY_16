"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

import csv
import pickle
import os
from .music_exam import MusicExam
from .serializer_interface import SerializerInterface


class MusicExamSerializer(SerializerInterface):
    """
    A class that provides serialization and deserialization \
functionality for MusicExam objects.

    This class implements the SerializerInterface and provides methods \
to serialize and deserialize
    MusicExam objects to/from CSV and pickle file formats.

    """
    @staticmethod
    def serialize_csv(exam: MusicExam, filename: str):
        """
        A class that provides serialization and deserialization \
functionality for MusicExam objects.

        This class implements the SerializerInterface and provides \
methods to serialize and deserialize
        MusicExam objects to/from CSV and pickle file formats.

        """
        cwd = os.getcwd()
        with open(cwd + '\\task1\\' + filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Instrument', 'Specialty'])
            for specialty, musicians in exam.get_applicants().items():
                for musician in musicians:
                    writer.writerow([musician.name, musician.instrument,
                                     specialty])

    @staticmethod
    def deserialize_csv(filename: str) -> MusicExam:
        """
        Deserialize a MusicExam object from a CSV file.

        Args:
            filename (str): The name of the CSV file to be deserialized.

        Returns:
            MusicExam: The deserialized MusicExam object.

        """
        exam = MusicExam()
        cwd = os.getcwd()
        with open(cwd + '\\task1\\' + filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name, instrument, specialty = row
                exam.add_applicant(name, instrument, specialty)
        return exam

    @staticmethod
    def serialize_pkl(exam: MusicExam, filename: str):
        """
        Serialize a MusicExam object to a pickle file.

        Args:
            exam (MusicExam): The MusicExam object to be serialized.
            filename (str): The name of the pickle file to be created.

        """
        cwd = os.getcwd()
        with open(cwd + '\\task1\\' + filename, 'wb') as file:
            pickle.dump(exam, file)

    @staticmethod
    def deserialize_pkl(filename: str) -> MusicExam:
        """
        Deserialize a MusicExam object from a pickle file.

        Args:
            filename (str): The name of the pickle file to be \
deserialized.

        Returns:
            MusicExam: The deserialized MusicExam object.

        """
        cwd = os.getcwd()
        with open(cwd + '\\task1\\' + filename, 'rb') as file:
            exam = pickle.load(file)
        return exam

    @staticmethod
    def serialize_dict_to_csv(applicants: dict, filename: str):
        """
        Serialize a dictionary of applicants to a CSV file.

        Args:
            applicants (dict): A dictionary containing applicant \
information, where the keys are applicant names and the values are \
tuples of (instrument, specialty).
            filename (str): The name of the CSV file to be created.

        """
        cwd = os.getcwd()
        with open(cwd + '\\task1\\' + filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Instrument', 'Specialty'])
            for name, (instrument, specialty) in applicants.items():
                writer.writerow([name, instrument, specialty])
