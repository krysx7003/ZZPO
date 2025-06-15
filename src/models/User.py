from typing import override


class User:
    """
    Represents a user in the blood donation system.

    Attributes:
        id: The unique identifier for the user.
        name: The user's first name.
        last_name: The user's last name.
        age: The user's age.
    """

    def __init__(self, name: str, lastName: str, age: int, userID: int = -1):
        """
        Initializes a User object.

        :param name: The user's first name.
        :param lastName: The user's last name.
        :param age: The user's age.
        :param userID: The unique identifier for the user (default: -1).
        """

        self.id: int = userID
        self.name: str = name
        self.last_name: str = lastName
        self.age: int = age

    def toDict(self):
        """
        Converts the user to a dictionary.

        :return: A dictionary representing the user.
        """

        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
        }

    @override
    def __str__(self):
        """
        Returns a string representation of the user.

        :return: A string with the user's name, last name, and age.
        """

        return f"{self.name} {self.last_name}, wiek {self.age}"

    def setID(self, user_id: int):
        """
        Sets the user ID.

        :param user_id: The new user ID.
        """

        self.id = user_id
