class DonationType:
    """
    Represents a type of blood donation.

    Attributes:
        id: The unique identifier for the donation type.
        name: The name of the donation type.
        max_amount: The maximum amount that can be donated for this type.
    """

    def __init__(self, donationTypeId: int, name: str, maxDonationAmount: int):
        """
        Initializes a DonationType object.

        :param donationTypeId: The unique identifier for the donation type.
        :param name: The name of the donation type.
        :param maxDonationAmount: The maximum amount that can be donated for this type.
        """

        self.id: int = donationTypeId
        self.name: str = name
        self.max_amount: int = maxDonationAmount

    def toDict(self):
        """
        Converts the donation type to a dictionary.

        :return: A dictionary representing the donation type.
        """

        return {"id": self.id, "name": self.name, "max_amount": self.max_amount}
