import tkinter as tk
from FrontEnd.Titlebar import darkTitleBar
from FrontEnd.Card import Card

def fillCardContent():
    # Example: Replace with your actual function logic!
    return [
        ["Krew pełna 500ml 22.06.2025", "Krew pełna 500ml 22.10.2025"],
        ["Osocze - Fact A", "Osocze - Fact B"],
        ["Płytki krwi - Line 1", "Płytki krwi - Line 2"],
        ["Krwinki czerwone - X", "Krwinki czerwone - Y"],
        ["Krwinki białe - I", "Krwinki białe - II"],
        ["Osocze i płytki - Alpha", "Osocze i płytki - Beta"]
    ]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ZZPOpuszczanieKrwi')
        self.geometry('400x400')
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

        self.cards = []
        buttonColors = [
            '#9c1057',
            '#f78104',
            '#0096c7',
            '#ff5883',
            '#2a9d8f',
            '#73a942'
        ]

        self.buttonFrame = tk.Frame(self, bg='#1e1e1e')
        self.buttonFrame.pack(expand=True)

        max_text_length = max(len(text) for text in buttonTexts)

        for i, text in enumerate(buttonTexts):
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
                width=max_text_length + 2,
                command=lambda i=i: self.showCard(i)
            )
            btn.pack(pady=6, anchor='center')

        # Fill card content at startup
        self.cardContent = fillCardContent()

    def showCard(self, cardNumber):
        # Hide all cards
        for card in self.cards:
            card.hide()

        # Get content for the selected card (join list into string)
        content_lines = self.cardContent[cardNumber]
        content_text = "\n".join(content_lines)

        self.cards[cardNumber].updateContent(content_text)
        self.cards[cardNumber].show()
