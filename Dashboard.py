import tkinter as tk
from tkinter import ttk

from database.DatabaseManager import get_database
from models.Donation import Donation


class Dashboard:
    def __init__(self, user_id: int):
        self.db = get_database()
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("Panel użytkownika - Oddawanie krwi")
        self.root.geometry("800x400")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text=f"Donacje użytkownika ID {self.user_id}", font=("Helvetica", 16)).pack(pady=10)

        columns = ("id", "type", "amount", "date")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        tree.heading("id", text="ID")
        tree.heading("type", text="Typ donacji")
        tree.heading("amount", text="Ilość (ml)")
        tree.heading("date", text="Data")

        donations = self.db.fetchUserDonnations(self.user_id)
        for d in donations:
            donation = Donation(**d)
            tree.insert("", "end", values=(
                donation.donationID,
                donation.donation_type_name,
                donation.amount,
                donation.date
            ))

        tree.pack(expand=True, fill="both", padx=20, pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # TEST - podaj ID użytkownika (np. 1)
    dashboard = Dashboard(user_id=1)
    dashboard.run()
