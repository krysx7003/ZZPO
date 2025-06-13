import tkinter as tk
from FrontEnd.Titlebar import darkTitleBar
from FrontEnd.Card import Card

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ZZPOpuszczanieKrwi')
        self.geometry('400x400')
        self.resizable(width=False, height=False)

        darkTitleBar(self)
        self.configure(bg='#1e1e1e')

        # List of different button texts
        button_texts = [
            "Krew pełna",
            "Osocze",
            "Płytki krwi",
            "Krwinki czerwone",
            "Krwinki białe",
            "Osocze i płytki"
        ]

        # List to hold Card instances, one card per button
        self.cards = []

        buttonColors = [
            '#9c1057',
            '#f78104',
            '#0096c7',
            '#ff5883',
            '#2a9d8f',
            '#73a942'
        ]

        # Frame to hold the buttons
        self.buttonFrame = tk.Frame(self, bg='#121212')
        self.buttonFrame.pack(expand=True)

        # Calculate max text length for uniform button width
        max_text_length = max(len(text) for text in button_texts)

        for i, text in enumerate(button_texts):
            card = Card(self)
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
                width=max_text_length + 2,  # uniform width in characters
                command=lambda i=i: self.showCard(i)
            )
            btn.pack(pady=6, anchor='center')

    def showCard(self, index):
        # Hide all cards first
        for card in self.cards:
            card.hide()

        # Define content for each card separately
        contentTexts = [
            "Informacje o Krwi pełnej",
            "Informacje o Osoczu",
            "Informacje o Płytkach krwi",
            "Informacje o Krwinkach czerwonych",
            "Informacje o Krwinkach białych",
            "Informacje o Osoczu i płytkach"
        ]

        # Update the selected card with its unique content
        self.cards[index].updateContent(contentTexts[index])
        self.cards[index].show()

