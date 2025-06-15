import tkinter as tk
from database.DatabaseManager import get_database
from models import Donation

class EditDonationForm(tk.Toplevel):
    def __init__(self, parent, donation_data):
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

    # Make the overlay cover the entire parent window and update on move
    def setFullscreenOverlay(self):
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

    # Update overlay position when the parent window moves
    def updateOverlayPosition(self, event):
        if not self.winfo_exists():
            return
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")

    def onClose(self):
        if self._bind_id:
            self.main_window.unbind("<Configure>", self._bind_id)
        self.destroy()

    def createWidgets(self):
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
