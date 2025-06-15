import tkinter as tk

from src.frontEnd.DonationCard import DonationCard
from src.frontEnd.Titlebar import darkTitleBar
from src.database.DatabaseManager import get_database

class App(tk.Tk):
    """
    Main application class for managing blood donation records.

    This class initializes the main window of the application, sets up the UI,
    and manages the display of donation cards for different types of blood donations.
    It uses Tkinter for the graphical interface and interacts with the database
    to fetch and display donation data.
    """

    def __init__(self):
        super().__init__()
        self.title("ZZPOpuszczanieKrwi")
        self.geometry("600x400")
        self.resizable(width=False, height=False)
        darkTitleBar(self)
        self.configure(bg="#1e1e1e")

        buttonTexts = [
            "Krew pełna",
            "Osocze",
            "Płytki krwi",
            "Krwinki czerwone",
            "Krwinki białe",
            "Osocze i płytki",
        ]
        buttonColors = [
            "#9c1057",
            "#f78104",
            "#0096c7",
            "#ff5883",
            "#2a9d8f",
            "#73a942",
        ]

        self.cards = []
        self.buttonFrame = tk.Frame(self, bg="#1e1e1e")
        self.buttonFrame.pack(expand=True)

        maxTextLength = max(len(text) for text in buttonTexts)
        self.cardContent = self.fillDonationCardContent()
        db = get_database()
        donation_types = db.fetchDonationTypes()  # Fetch types to get IDs

        for i, text in enumerate(buttonTexts):
            type_id = donation_types[i].id  # Get the type ID for this card
            card = DonationCard(self, self.cardContent[i], buttonTexts[i], type_id, db)
            self.cards.append(card)
            btn = tk.Button(
                self.buttonFrame,
                text=text,
                bg=buttonColors[i],
                fg="white",
                relief="flat",
                bd=0,
                highlightthickness=0,
                padx=20,
                pady=12,
                font=("Segoe UI", 12, "bold"),
                width=maxTextLength + 2,
                command=lambda i=i: self.showCard(i),
            )
            btn.pack(pady=6, anchor="center")

    def fillDonationCardContent(self):
        """
        Function, that fetches all the donations information from the database.
        :return: Data about donations from the database.
        """
        db = get_database()
        allDonations = db.fetchAllDonations()

        # Initialize lists for each donation type
        pelna = []
        osocze = []
        plytki = []
        krwinkic = []
        krwinkib = []
        osoczeiplytki = []

        # Map type IDs to lists
        donation_groups = {
            1: pelna,
            2: osocze,
            3: plytki,
            4: krwinkic,
            5: krwinkib,
            6: osoczeiplytki
        }

        # Group donations
        for donation in allDonations:
            group = donation_groups.get(donation.donation_typeID)
            if group is not None:
                group.append((
                    donation.donationID,
                    donation.donation_typeID,
                    donation.amount,
                    donation.date,
                    donation.userID
                ))

        return [pelna, osocze, plytki, krwinkic, krwinkib, osoczeiplytki]

    def showCard(self, cardNumber):
        """
        Shows the DonationCard for the cardNumber instance.
        :param cardNumber: Number of the DonationCard:
                           1-Krew pełna,
                           2-Osocze,
                           3-Płytki krwi,
                           4-Krwiniki czerwone,
                           5-Krwinki białe,
                           6-Osocze i płytki
        """
        for card in self.cards:
            card.hide()
        self.cards[cardNumber].show()
