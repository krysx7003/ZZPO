import tkinter as tk
from FrontEnd.Titlebar import darkTitleBar
from FrontEnd.DonationCard import DonationCard

def fillDonationCardContent():
    # Example entries data
    return [
        [ (1, 101, 500, "2025-06-22", 1001), (2, 101, 500, "2025-10-22", 1001) ],  # Krew pełna
        [ (3, 102, 300, "2025-06-22", 1002), (4, 102, 250, "2025-07-10", 1003) ],  # Osocze
        [ (5, 103, 200, "2025-06-15", 1004), (6, 103, 180, "2025-06-16", 1005) ],  # Płytki krwi
        [ (7, 104, 450, "2025-06-14", 1006), (8, 104, 400, "2025-06-18", 1007) ],  # Krwinki czerwone
        [ (9, 105, 350, "2025-06-12", 1008), (10, 105, 340, "2025-06-13", 1009) ], # Krwinki białe
        [ (11, 106, 600, "2025-06-11", 1010), (12, 106, 620, "2025-06-19", 1011) ] # Osocze i płytki
    ]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ZZPOpuszczanieKrwi')
        self.geometry('600x400')
        self.resizable(width=False, height=False)

        darkTitleBar(self)
        self.configure(bg='#1e1e1e')

        buttonTexts = [
            "Krew pełna",
            "Osocze",
            "Płytki krwi",
            "Krwinki czerwone",
            "Krwinki białe",
            "Osocze i płytki"
        ]

        buttonColors = [
            '#9c1057',
            '#f78104',
            '#0096c7',
            '#ff5883',
            '#2a9d8f',
            '#73a942'
        ]

        self.cards = []
        self.buttonFrame = tk.Frame(self, bg='#1e1e1e')
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
                fg='white',
                relief='flat',
                bd=0,
                highlightthickness=0,
                padx=20,
                pady=12,
                font=('Segoe UI', 12, 'bold'),
                width=maxTextLength + 2,
                command=lambda i=i: self.showCard(i)
            )
            btn.pack(pady=6, anchor='center')

    def showCard(self, cardNumber):
        # Hide all cards
        for card in self.cards:
            card.hide()

        # Show the selected card
        self.cards[cardNumber].show()
