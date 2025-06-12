class DonationType:
    def __init__(self, donation_typeID: int, name: str, max_amount: int):
        self.id = donation_typeID
        self.name = name
        self.max_amount = max_amount

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_amount": self.max_amount
        }
