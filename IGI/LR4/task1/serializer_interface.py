"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

from abc import ABC, abstractmethod


class SerializerInterface(ABC):
    """
    An abstract base class representing a serializer interface.

    Methods:
        serialize_csv(obj, file): Serialize an object to a CSV file.
        deserialize_csv(file): Deserialize an object from a CSV file.
        serialize_pkl(obj, file): Serialize an object to a pickle file.
        deserialize_pkl(file): Deserialize an object from a pickle file.
        serialize_dict_to_csv(obj, file): Serialize a dictionary to a \
CSV file.

    """
    @staticmethod
    @abstractmethod
    def serialize_csv(obj, file):
        """
        Serialize an object to a CSV file.

        Args:
            obj: The object to be serialized.
            file: The name or file-like object of the CSV file to be \
created.

        """
        pass

    @staticmethod
    @abstractmethod
    def deserialize_csv(file):
        """
        Deserialize an object from a CSV file.

        Args:
            file: The name or file-like object of the CSV file to be \
deserialized.

        Returns:
            The deserialized object.

        """
        pass

    @staticmethod
    @abstractmethod
    def serialize_pkl(obj, file):
        """
        Serialize an object to a pickle file.

        Args:
            obj: The object to be serialized.
            file: The name or file-like object of the pickle file to \
be created.

        """
        pass

    @staticmethod
    @abstractmethod
    def deserialize_pkl(file):
        """
        Deserialize an object from a pickle file.

        Args:
            file: The name or file-like object of the pickle file to \
be deserialized.

        Returns:
            The deserialized object.

        """
        pass

    @staticmethod
    @abstractmethod
    def serialize_dict_to_csv(obj, file):
        """
        Serialize a dictionary to a CSV file.

        Args:
            obj: The dictionary to be serialized.
            file: The name or file-like object of the CSV file to be \
created.

        """
        pass
