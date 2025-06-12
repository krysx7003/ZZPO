import tkinter as tk
from tkinter import ttk

from database.DatabaseManager import get_database
from models.Donation import Donation
from models.User import User


class Dashboard:
    def __init__(self, user_id: int):
        self.db = get_database()
        self.user_id = user_id
        self.user = self.get_user_info()
        self.root = tk.Tk()
        self.root.title("Panel użytkownika - Oddawanie krwi")
        self.root.geometry("800x500")
        self.setup_ui()

    def get_user_info(self):
        data = self.db.fetchUserById(self.user_id)
        if data:
            return User(**data)
        else:
            raise ValueError(f"Użytkownik o ID {self.user_id} nie istnieje")

    def setup_ui(self):
        # Informacje o użytkowniku
        user_info_frame = tk.Frame(self.root)
        user_info_frame.pack(pady=10)

        tk.Label(user_info_frame, text=f"Użytkownik: {self.user.name} {self.user.last_name}", font=("Helvetica", 14)).pack()
        tk.Label(user_info_frame, text=f"Wiek: {self.user.age} | ID: {self.user.id}", font=("Helvetica", 12)).pack()

        # Tabela z donacjami
        tk.Label(self.root, text="Historia donacji", font=("Helvetica", 16)).pack(pady=10)

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
    dashboard = Dashboard(user_id=1)
    dashboard.run()
