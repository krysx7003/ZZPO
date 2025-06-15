class Donation:
    """
    Represents a blood donation record.

    Attributes:
        donationID: The unique identifier for the donation.
        donation_typeID: The type of donation.
        amount: The amount of blood donated.
        date: The date of the donation.
        userID: The ID of the user who donated.
    """

    def __init__(self, donation_typeID: int, amount: int, date: str, userID: int, donationID: int = -1):
        """
        Initializes a Donation object.

        :param donation_typeID: The type of donation.
        :param amount: The amount of blood donated.
        :param date: The date of the donation.
        :param userID: The ID of the user who donated.
        :param donationID: The unique identifier for the donation (default: -1).
        """

        self.donationID: int = donationID
        self.donation_typeID: int = donation_typeID
        self.amount: int = amount
        self.date: str = date
        self.userID: int = userID

    def setID(self, donnation_id: int):
        """
        Sets the donation ID.

        :param donnation_id: The new donation ID.
        """

        self.donationID = donnation_id
