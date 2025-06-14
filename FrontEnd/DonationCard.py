import tkinter as tk
from tkinter import ttk

from FrontEnd.DonationForm import DonationForm

class DonationCard(tk.Frame):
    def __init__(self, parent, data, title):
        super().__init__(parent, bg='#1e1e1e')
        self.data = data
        if data and len(data) > 0 and len(data[0]) > 1:
            self.donation_typeID = data[0][1]
        else:
            self.donation_typeID = None

        self.title = title

        # Display the title above the TreeView if provided
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

        # Action Button
        action_btn = tk.Button(
            buttons_frame,
            text="Add entry",
            command=self.onAction,
            bg="#444444",
            fg="white",
            relief="flat",
            width=btn_width,
        )
        action_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # Close Button
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
        # Remove all previous rows
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert new data
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def onAction(self):
        if not self.donation_typeID:
            print("Error: No donation type associated with this card")
            return

        DonationForm(self, self.donation_typeID)
        self.focus_set()  # Keep card focused behind the form

    def show(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.lift()

    def hide(self):
        self.place_forget()
