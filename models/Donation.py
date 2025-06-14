class Donation:
    def __init__(
        self, donationID, donation_typeID, amount, date, userID, donation_type_name=None
    ):
        self.donationID = donationID
        self.donation_typeID = donation_typeID
        self.amount = amount
        self.date = date
        self.userID = userID
        self.donation_type_name = donation_type_name
