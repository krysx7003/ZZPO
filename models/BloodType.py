class BloodType:
    def __init__(self, blood_typeID: int, name: str):
        self.id: int = blood_typeID
        self.name: str = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}
