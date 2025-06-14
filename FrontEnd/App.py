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

    # Initializee lists for each donation type
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

    print(pelna, osocze, plytki, krwinkic, krwinkib, osoczeiplytki)

    return [pelna, osocze, plytki, krwinkic, krwinkib, osoczeiplytki]


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
