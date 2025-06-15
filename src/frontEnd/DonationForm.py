import tkinter as tk
from database.DatabaseManager import get_database
from models import Donation

class DonationForm(tk.Toplevel):
    def __init__(self, parent, donation_typeID):
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

    # Make the overlay cover the entire parent window and update on move
    def setFullscreenOverlay(self):
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")  # Note: Typo fixed below

        # Bind to main window's movement events
        self.main_window = self.parent.winfo_toplevel()
        self._bind_id = self.main_window.bind(
            "<Configure>",
            self.updateOverLayPosition
        )

    # Update overlay position when the parent window moves
    def updateOverLayPosition(self, event):
        if not self.winfo_exists():
            return
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")  # Fixed: parent1_width -> parent_width

    def onClose(self):
        if self._bind_id:
            self.main_window.unbind("<Configure>", self._bind_id)
        self.destroy()

    def createWidgets(self):
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
        tk.Button(btn_frame, text="Submit", command=self.submit).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(
            side=tk.RIGHT, padx=5
        )

    def submit(self):
        try:
            db = get_database()
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
