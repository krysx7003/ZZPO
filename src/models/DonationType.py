class DonationType:
    def __init__(self, donation_typeID: int, name: str, max_amount: int):
        self.id: int = donation_typeID
        self.name: str = name
        self.max_amount: int = max_amount

    def to_dict(self):
        return {"id": self.id, "name": self.name, "max_amount": self.max_amount}
