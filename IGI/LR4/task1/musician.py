"""
Lab: 4
Version: 1.0.0
Author: Petrovsky, 253505
Date: 10.04.2024
"""

class Musician:
    """
    Represents a musician with a name and an instrument.

    Attributes:
        _name (str): The name of the musician.
        _instrument (str): The instrument played by the musician.

    Methods:
        __eq__(self, other): Compares two Musician objects based on \
the instrument.
        __ne__(self, other): Compares two Musician objects based on \
the instrument.
        name: Property to get and set the name of the musician.
        instrument: Property to get and set the instrument of the \
musician.

    """
    def __init__(self, name: str, instrument: str):
        """
        Initializes a Musician object.

        Args:
            name (str): The name of the musician.
            instrument (str): The instrument played by the musician.

        """
        self._name = name
        self._instrument = instrument

    def __eq__(self, other):
        """
        Compares two Musician objects based on the instrument.

        Args:
            other (Musician): The other Musician object to compare with.

        Returns:
            bool: True if the instruments are the same, False otherwise.

        Raises:
            TypeError: If the other object is not an instance of Musician.

        """
        if isinstance(other, Musician):
            return self.instrument == other.instrument
        raise TypeError("Cannot compare objects of different types")

    def __ne__(self, other):
        """
        Compares two Musician objects based on the instrument.

        Args:
            other (Musician): The other Musician object to compare with.

        Returns:
            bool: True if the instruments are different, False otherwise.

        Raises:
            TypeError: If the other object is not an instance of Musician.

        """
        if isinstance(other, Musician):
            return not self.__eq__(other)
        raise TypeError("Cannot compare objects of different types")

    @property
    def name(self):
        """
        Gets the name of the musician.

        Returns:
            str: The name of the musician.

        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Sets the name of the musician.

        Args:
            value (str): The new name of the musician.

        Raises:
            ValueError: If the new name is not a non-empty string.

        """
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Invalid name. It must be a non-empty string.")

    @property
    def instrument(self):
        """
        Gets the instrument played by the musician.

        Returns:
            str: The instrument played by the musician.

        """
        return self._instrument

    @instrument.setter
    def instrument(self, value: str):
        """
        Sets the instrument played by the musician.

        Args:
            value (str): The new instrument played by the musician.

        Raises:
            ValueError: If the new instrument is not a non-empty string.

        """
        if isinstance(value, str) and len(value) > 0:
            self._instrument = value
        else:
            raise ValueError("Invalid instrument. It must be a non-empty \
string.")
