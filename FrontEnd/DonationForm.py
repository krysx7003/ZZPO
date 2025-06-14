import tkinter as tk

from database.DatabaseManager import get_database
from models import Donation


class DonationForm(tk.Toplevel):
    def __init__(self, parent, donation_typeID):
        super().__init__(parent)
        self.donation_typeID = donation_typeID
        self.parent = parent  # Reference to DonationCard
        self.title("New Donation Entry")
        self.configure(bg='#1e1e1e')
        self._create_widgets()
        self._center_on_card()

    def _center_on_card(self):
        """Center the form over the parent DonationCard"""
        self.update_idletasks()
        card_x = self.parent.winfo_rootx()
        card_y = self.parent.winfo_rooty()
        card_width = self.parent.winfo_width()

        x = card_x + (card_width // 2) - (self.winfo_width() // 2)
        y = card_y + 50  # Offset from top of card
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        fields = [
            ("Amount (ml):", "amount"),
            ("Date (YYYY-MM-DD):", "date"),
            ("User ID:", "userID")
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(self, text=label, bg='#1e1e1e', fg='white').grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        btn_frame = tk.Frame(self, bg='#1e1e1e')
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)

        tk.Button(btn_frame, text="Submit", command=self._submit).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _submit(self):
        try:
            db = get_database()
            new_donation = Donation(
                donation_typeID=self.donation_typeID,
                amount=int(self.entries['amount'].get()),
                date=self.entries['date'].get(),
                userID=int(self.entries['userID'].get())
            )

            db.addDonation(new_donation)
            # Update parent card's data directly
            self.parent.data.append((
                new_donation.donationID,
                self.donation_typeID,
                new_donation.amount,
                new_donation.date,
                new_donation.userID
            ))
            self.parent.insertData(self.parent.data)

        except ValueError as e:
            print(f"Validation error: {e}")
        finally:
            self.destroy()
