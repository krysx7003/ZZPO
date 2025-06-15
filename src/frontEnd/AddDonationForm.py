import tkinter as tk

from database.DatabaseManager import getDatabase
from models import Donation


class DonationForm(tk.Toplevel):
    """
    A form window for creating new blood donation entries.

    This class provides a modal overlay form that allows users to input new donation data
    for a specific donation type. The form is centered over the parent card and follows
    the parent window when it is moved or resized.
    """

    def __init__(self, parent, donation_typeID):
        """
        Initializes the AddDonationForm window.

        :param parent: The parent widget (typically a DonationCard instance).
        :param donation_typeID: The ID of the donation type for this entry.
        """

        super().__init__(parent)
        self.donation_typeID = donation_typeID
        self.parent = parent  # Reference to DonationCard
        self.title("New Donation Entry")
        self.configure(bg="#1e1e1e")
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self.setFullscreenOverlay()
        self.createWidgets()
        self.grab_set()  # Modal overlay
        self._bind_id = None

        # Add cleanup on window close
        self.protocol("WM_DELETE_WINDOW", self.onClose)

    def setFullscreenOverlay(self):
        """
        Makes the form overlay cover the entire parent window and binds to the parent's movement events.

        The overlay is positioned and sized to match the parent window, and will update its position
        whenever the parent window is moved or resized.
        """

        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.geometry(
            f"{parent_width}x{parent_height}+{parent_x}+{parent_y}"
        )  # Note: Typo fixed below

        # Bind to main window's movement events
        self.main_window = self.parent.winfo_toplevel()
        self._bind_id = self.main_window.bind("<Configure>", self.updateOverLayPosition)

    # Update overlay position when the parent window moves
    def updateOverLayPosition(self):
        """
        Updates the overlay's position and size to match the parent window.

        :param event: The event that triggered this update (optional).
        """

        if not self.winfo_exists():
            return
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.geometry(
            f"{parent_width}x{parent_height}+{parent_x}+{parent_y}"
        )  # Fixed: parent1_width -> parent_width

    def onClose(self):
        """
        Cleans up resources and closes the form window.

        Unbinds from the parent window's movement events and destroys the form.
        """

        if self._bind_id:
            self.main_window.unbind("<Configure>", self._bind_id)
        self.destroy()

    def createWidgets(self):
        """
        Creates and lays out the widgets for the donation form.

        Includes entry fields for amount, date, and user ID, as well as submit and cancel buttons.
        """

        # Create a semi-transparent background frame to dim the content
        overlay = tk.Frame(self, bg="#1e1e1e")
        overlay.place(relwidth=1, relheight=1)

        # Center the actual form in the overlay
        form_frame = tk.Frame(overlay, bg="#222", bd=2, relief="ridge")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        fields = [
            ("Amount (ml):", "amount"),
            ("Date (YYYY-MM-DD):", "date"),
            ("User ID:", "userID"),
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            btn_frame = tk.Frame(self, bg="#1e1e1e")
            tk.Label(form_frame, text=label, bg="#222", fg="white").grid(
                row=i, column=0, padx=10, pady=5
            )
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        btn_frame = tk.Frame(form_frame, bg="#222")
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)
        tk.Button(btn_frame, text="Submit", command=self.onSubmit).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(
            side=tk.RIGHT, padx=5
        )

    def onSubmit(self):
        """
        Handles the submission of the donation form.

        Validates the input, creates a new donation record in the database,
        and updates the parent card's data. Closes the form when done.
        """

        try:
            db = getDatabase()
            new_donation = Donation(
                donation_typeID=self.donation_typeID,
                amount=int(float(self.entries["amount"].get())),
                date=self.entries["date"].get(),
                userID=int(self.entries["userID"].get()),
            )
            new_id = db.addDonation(new_donation)
            # Update parent card's data directly
            self.parent.data.append(
                (
                    new_id,
                    self.donation_typeID,
                    new_donation.amount,
                    new_donation.date,
                    new_donation.userID,
                )
            )
            self.parent.insertData(self.parent.data)
        except ValueError as e:
            print(f"Validation error: {e}")
        finally:
            self.destroy()
