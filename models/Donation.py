class Donation:
    def __init__(
        self,
        donation_typeID: int,
        amount: int,
        date: str,
        userID: int,
        donationID: int = -1,
    ):
        self.donationID: int = donationID
        self.donation_typeID: int = donation_typeID
        self.amount: int = amount
        self.date: str = date
        self.userID: int = userID

    def setID(self, donnation_id: int):
        self.donationID = donnation_id
