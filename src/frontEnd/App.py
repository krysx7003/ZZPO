import tkinter as tk

from database.DatabaseManager import getDatabase
from frontEnd.DonationCard import DonationCard
from frontEnd.Titlebar import darkTitleBar


class App(tk.Tk):
    """
    Main application class for managing blood donation records.

    This class initializes the main window of the application, sets up the UI,
    and manages the display of donation cards for different types of blood donations.
    It uses Tkinter for the graphical interface and interacts with the database
    to fetch and display donation data.
    """

    def __init__(self):
        """
        Initializes the main application window.

        Sets up the window title, size, and style, and creates a frame for navigation buttons.
        Instantiates donation cards for each donation type and populates them with data from the database.
        Each card is associated with a button that allows the user to display the corresponding donation data.
        """

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
        self.value_labels = []
        self.buttonFrame = tk.Frame(self, bg="#1e1e1e")
        self.buttonFrame.pack(expand=True)

        maxTextLength = max(len(text) for text in buttonTexts)
        self.cardContent = self.fillDonationCardContent()
        db = getDatabase()
        donation_types = db.fetchDonationTypes()  # Fetch types to get IDs
        last_donation = self.getLastDonationDate()

        for i, text in enumerate(buttonTexts):
            type_id = donation_types[i].id
            card = DonationCard(self, self.cardContent[i], buttonTexts[i], type_id, db)
            self.cards.append(card)

            # Główna ramka dla całego wiersza
            row_frame = tk.Frame(self.buttonFrame, bg="#1e1e1e")
            row_frame.pack(
                fill="x", pady=6, anchor="w"
            )  # anchor="w" do wyrównania do lewej

            # PRZYCISK
            btn = tk.Button(
                row_frame,  # Zmiana rodzica na row_frame
                text=text,
                bg=buttonColors[i],
                fg="white",
                relief="flat",
                font=("Segoe UI", 12, "bold"),
                width=maxTextLength + 2,
                command=lambda i=i: self.showCard(i),
            )
            btn.pack(side="left", padx=(0, 10))  # Margines prawy 10px

            # ETYKIETA Z WARTOŚCIĄ
            # Twoja metoda pobierająca wartość
            label = tk.Label(
                row_frame,  # Zmiana rodzica na row_frame
                text=str(self.calculateTimeForNextDonation(last_donation, i + 1)),
                bg="#1e1e1e",
                fg="white",
                font=("Segoe UI", 8),
                width=20,  # Stała szerokość dla wyrównania
            )
            label.pack(side="left")
            self.value_labels.append(label)

    def fillDonationCardContent(self):
        """
        Function, that fetches all the donations information from the database.
        :return: Data about donations from the database.
        """
        db = getDatabase()
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
            6: osoczeiplytki,
        }

        # Group donations
        for donation in allDonations:
            group = donation_groups.get(donation.donation_typeID)
            if group is not None:
                group.append(
                    (
                        donation.donationID,
                        donation.donation_typeID,
                        donation.amount,
                        donation.date,
                        donation.userID,
                    )
                )

        return [pelna, osocze, plytki, krwinkic, krwinkib, osoczeiplytki]

    def getLastDonationDate(self):
        """
        Returns the date of the last donation from the database.
        """
        db = getDatabase()
        all_donations = db.fetchAllDonations()
        if not all_donations:
            return None
        last_donation = max(all_donations, key=lambda d: d.date)
        return last_donation.date if last_donation else None

    def getLastDonationType(self, last_donation):
        """
        Returns the date of the last donation from the database.
        """
        db = getDatabase()
        all_donations = db.fetchAllDonations()
        if not all_donations:
            return None
        last_donation = max(all_donations, key=lambda d: d.date)
        if last_donation:
            return last_donation.donation_typeID
        return None

    def calculateTimeForNextDonation(self, last_donation, i):
        """
        Calculates the time remaining until the next donation based on the last donation date and type.
        :param last_donation: List containing the last donation date and type ID.
        :return: Time remaining until the next donation in days.
        """
        if not last_donation:
            return "N/A"

        from datetime import datetime, timedelta

        last_date = datetime.strptime(last_donation, "%Y-%m-%d")

        # Define donation intervals based on type
        intervals = {
            1: 56,  # Krew pełna
            2: 14,  # Osocze
            3: 14,  # Płytki krwi
            4: 56,  # Krwinki czerwone
            5: 14,  # Krwinki białe
            6: 14,  # Osocze i płytki
        }
        today = datetime.now() + timedelta(
            days=1
        )  # Adding one day to include today in the calculation
        days_since_last = (today - last_date).days
        days_until_next = intervals[i] - days_since_last
        return (
            f"Zostało {days_until_next} dni"
            if days_until_next > 0
            else "Możesz oddać krew!"
        )

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

    def update_value_labels(self):
        last_donation = self.getLastDonationDate()
        for i, label in enumerate(self.value_labels):
            label.config(text=str(self.calculateTimeForNextDonation(last_donation, i + 1)))
