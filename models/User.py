from typing import override


class User:
    def __init__(self, name: str, last_name: str, age: int, userID: int = -1):
        self.id: int = userID
        self.name: str = name
        self.last_name: str = last_name
        self.age: int = age

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
        }

    @override
    def __str__(self):
        return f"{self.name} {self.last_name}, wiek {self.age}"
