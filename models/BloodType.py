class BloodType:
    def __init__(self, blood_typeID: int, name: str):
        self.id = blood_typeID
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}
