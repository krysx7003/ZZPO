import tkinter as tk
from database.DatabaseManager import get_database
from models import Donation

class EditDonationForm(tk.Toplevel):
    """
    A modal form for editing existing blood donation entries.

    This class provides a modal overlay window that allows users to modify
    the details of a selected donation. The form is styled with a dark theme
    and updates the database and parent card data upon submission.
    """

    def __init__(self, parent, donation_data):
        """
        Initializes the EditDonationForm window.

        :param parent: The parent widget (typically a DonationCard instance).
        :param donation_data: Dictionary containing the donation data to edit.
        """

        super().__init__(parent)
        self.parent = parent
        self.donation_data = donation_data
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self.configure(bg='#1e1e1e')
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
        self.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")

        # Bind to main window's movement events
        self.main_window = self.parent.winfo_toplevel()
        self._bind_id = self.main_window.bind(
            "<Configure>",
            self.updateOverlayPosition
        )

    def updateOverlayPosition(self):
        """
        Updates the overlay's position and size to match the parent window.
        """

        if not self.winfo_exists():
            return
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")

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
        Creates and lays out the widgets for the edit donation form.

        Includes entry fields for amount, date, and user ID, as well as save and cancel buttons.
        The fields are pre-filled with the current donation data.
        """

        overlay = tk.Frame(self, bg='#1e1e1e')
        overlay.place(relwidth=1, relheight=1)
        form_frame = tk.Frame(overlay, bg='#222', bd=2, relief='ridge')
        form_frame.place(relx=0.5, rely=0.5, anchor='center')

        fields = [
            ("Amount (ml):", "amount"),
            ("Date (YYYY-MM-DD):", "date"),
            ("User ID:", "userID"),
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(form_frame, text=label, bg='#222', fg='white').grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(form_frame)
            entry.insert(0, str(self.donation_data[field]))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        btn_frame = tk.Frame(form_frame, bg='#222')
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)
        tk.Button(btn_frame, text="Save", command=self.onSubmit).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def onSubmit(self):
        """
        Handles the submission of the edit donation form.

        Validates the input, updates the donation record in the database,
        and refreshes the parent card's data. Closes the form when done.
        :raises ValueError: If input validation fails.
        """

        try:
            db = get_database()
            updated_donation = Donation(
                donation_typeID=self.donation_data["donation_typeID"],
                amount=int(self.entries['amount'].get()),
                date=self.entries['date'].get(),
                userID=int(self.entries['userID'].get()),
                donationID=self.donation_data["donationID"]
            )
            db.editDonation(self.donation_data["donationID"], updated_donation)
            # Update parent card's data and refresh table
            for i, row in enumerate(self.parent.data):
                if row[0] == self.donation_data["donationID"]:
                    self.parent.data[i] = (
                        self.donation_data["donationID"],
                        self.donation_data["donation_typeID"],
                        updated_donation.amount,
                        updated_donation.date,
                        updated_donation.userID
                    )
                    break
            self.parent.insertData(self.parent.data)
        except ValueError as e:
            print(f"Validation error: {e}")
        finally:
            self.destroy()
