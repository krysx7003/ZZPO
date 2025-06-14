import tkinter as tk
from tkinter import ttk

class DonationCard(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent, bg='#1e1e1e')
        columns = ("DONATION_ID", "TYPE_ID", "AMOUNT", "DATE", "USER_ID")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        for row in data:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        close_btn = tk.Button(self, text="Close", command=self.hide, bg='#333333', fg='white', relief='flat')
        close_btn.pack(pady=(0, 10))

    def show(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.lift()

    def hide(self):
        self.place_forget()
