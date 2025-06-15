import tkinter as tk
from tkinter import ttk

from frontEnd.AddDonationForm import DonationForm
from frontEnd.EditDonationForm import EditDonationForm


class DonationCard(tk.Frame):
    """
    GUI component for displaying and managing donation entries of a specific blood donation type.

    This class creates a card interface using Tkinter's Frame widget that shows donation records in a Treeview.
    It provides functionality to add, edit, delete, and view donation entries associated with a particular donation type.
    The card is styled with a dark theme and interacts with a database to update donation data.
    """

    def __init__(self, parent, data, title, donation_typeID, db):
        """
        Initializes the DonationCard GUI component.

        Sets up the card with a dark-themed Treeview to display donation entries for a specific blood donation type.
        Creates buttons for adding, editing, deleting, and closing the card.
        Initializes the card with provided data, title, donation type ID, and database connection.

        :param parent: The parent widget in which this card will be placed.
        :param data: List of donation entries to display.
        :param title: Title of the card, displayed at the top.
        :param donation_typeID: The ID of the donation type this card represents.
        :param db: Database connection object for data operations.
        """

        super().__init__(parent, bg="#1e1e1e")
        self.data = data
        self.donation_typeID = donation_typeID
        self.title = title
        self.db = db

        if title:
            title_label = tk.Label(
                self,
                text=title,
                bg="#1e1e1e",
                fg="white",
                font=("Segoe UI", 14, "bold"),
            )
            title_label.pack(pady=(12, 0))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            fieldbackground="#1e1e1e",
            bordercolor="#1e1e1e",
            borderwidth=1,
        )
        style.map(
            "Treeview",
            background=[("selected", "#555555")],
            foreground=[("selected", "white")],
        )
        style.configure(
            "Treeview.Heading", background="#1e1e1e", foreground="white", relief="flat"
        )
        style.map("Treeview.Heading", background=[("active", "#555555")])

        columns = ("DONATION_ID", "TYPE_ID", "AMOUNT", "DATE", "USER_ID")
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", style="Treeview"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.insertData(self.data)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = tk.Frame(self, bg="#1e1e1e")
        buttons_frame.pack(pady=(0, 10), fill="x", padx=10)
        btn_width = 15

        action_btn = tk.Button(
            buttons_frame,
            text="Add entry",
            command=self.onAddEntry,
            bg="#444444",
            fg="white",
            relief="flat",
            width=btn_width,
        )
        action_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        edit_btn = tk.Button(
            buttons_frame,
            text="Edit entry",
            command=self.onEditEntry,
            bg="#555555",
            fg="white",
            relief="flat",
            width=btn_width,
        )
        edit_btn.pack(side="left", expand=True, fill="x", padx=(5, 5))

        delete_btn = tk.Button(
            buttons_frame,
            text="Delete entry",
            command=self.onDeleteEntry,
            bg="#666666",
            fg="white",
            relief="flat",
            width=btn_width,
        )
        delete_btn.pack(side="left", expand=True, fill="x", padx=(5, 5))

        close_btn = tk.Button(
            buttons_frame,
            text="Close",
            command=self.hide,
            bg="#333333",
            fg="white",
            relief="flat",
            width=btn_width,
        )
        close_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def insertData(self, data):
        """
        Inserts the provided donation data into the Treeview widget.

        :param data: List of donation entries to display.
        """

        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def onAddEntry(self):
        """
        Opens the form for adding a new donation entry.
        """

        DonationForm(self, self.donation_typeID)
        self.focus_set()

    def onEditEntry(self):
        """
        Opens the form for editing the selected donation entry.
        If no entry is selected, prints a message to the console.
        """

        selected = self.tree.selection()
        if not selected:
            print("No entry selected for editing")
            return
        values = self.tree.item(selected[0], "values")
        donation_data = {
            "donationID": int(values[0]),
            "donation_typeID": int(values[1]),
            "amount": int(float(values[2])),
            "date": values[3],
            "userID": int(values[4]),
        }
        EditDonationForm(self, donation_data)
        self.focus_set()

    def onDeleteEntry(self):
        """
        Deletes the selected donation entry from the database and the Treeview.
        If no entry is selected, prints a message to the console.
        """

        selected = self.tree.selection()
        if not selected:
            print("No entry selected for deletion")
            return
        # Get the donation ID from the first column (DONATION_ID)
        donation_id = int(self.tree.item(selected[0], "values")[0])
        # Delete from database
        self.db.deleteDonation(donation_id)
        # Remove from treeview
        self.tree.delete(selected[0])
        # Remove from self.data - using list comprehension
        self.data = [item for item in self.data if item[0] != donation_id]

    def show(self):
        """
        Makes the card visible and brings it to the front.
        """

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.lift()

    def hide(self):
        """
        Hides the card from view.
        """

        self.place_forget()
