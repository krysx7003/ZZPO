class User:
    def __init__(self, userID: int, name: str, last_name: str, age: int):
        self.id = userID
        self.name = name
        self.last_name = last_name
        self.age = age

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age
        }

    def __str__(self):
        return f"{self.name} {self.last_name}, wiek {self.age}"
