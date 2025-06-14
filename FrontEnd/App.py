import tkinter as tk

from FrontEnd.DonationCard import DonationCard
from FrontEnd.Titlebar import darkTitleBar
from database.DatabaseManager import get_database

def fillDonationCardContent():

    db = get_database()
    donation_types = db.fetchDonationTypes()
    for dtype in donation_types:
        print(dtype.id)
    allDonations = db.fetchAllDonations()
    for donation in allDonations:
        print(donation.donation_typeID)

    pelna = []
    osocze = []
    plytki = []
    krwinkic = []
    krwinkib = []
    osoczeiplytki = []

    for donation in allDonations:
        if donation.donation_typeID == 1:
            pelna.append((donation.donationID, donation.donation_typeID, donation.amount, donation.date, donation.userID))
        if donation.donation_typeID == 2:
            osocze.append((donation.donationID, donation.donation_typeID, donation.amount, donation.date, donation.userID))
        if donation.donation_typeID == 3:
            plytki.append((donation.donationID, donation.donation_typeID, donation.amount, donation.date, donation.userID))
        if donation.donation_typeID == 4:
            krwinkic.append((donation.donationID, donation.donation_typeID, donation.amount, donation.date, donation.userID))
        if donation.donation_typeID == 5:
            krwinkib.append((donation.donationID, donation.donation_typeID, donation.amount, donation.date, donation.userID))
        if donation.donation_typeID == 6:
            osoczeiplytki.append((donation.donationID, donation.donation_typeID, donation.amount, donation.date, donation.userID))
    print(pelna, osocze, plytki, krwinkic, krwinkib, osoczeiplytki)

    return [
        [
            pelna
        ],  # Krew pełna
        [
            osocze
        ],  # Osocze
        [
            plytki
        ],  # Płytki krwi
        [
            krwinkic
        ],  # Krwinki czerwone
        [
            krwinkib
        ],  # Krwinki białe
        [
            osoczeiplytki
        ],  # Osocze i płytki
    ]


class App(tk.Tk):
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

        # Prepare tabular data for each card
        self.cardContent = fillDonationCardContent()

        for i, text in enumerate(buttonTexts):
            card = DonationCard(self, self.cardContent[i], buttonTexts[i])
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

    def showCard(self, cardNumber):
        # Hide all cards
        for card in self.cards:
            card.hide()

        # Show the selected card
        self.cards[cardNumber].show()
