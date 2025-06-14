import tkinter as tk


class Card(tk.Frame):

    # Constructor takes parent widget
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")

        # Label widget inside the card to display temporary text
        self.label = tk.Label(
            self,
            # Default text
            text="Card Content",
            # Card background colour
            bg="#1e1e1e",
            # White text color
            fg="white",
        )
        self.label.pack(padx=10, pady=(10, 5))

        # Close button to hide the card overlay
        self.close_button = tk.Button(
            self,
            # Default text
            text="Close",
            # Bind click to hide method
            command=self.hide,
            # Dark gray background
            bg="#333333",
            # White text
            fg="white",
            # Flat style
            relief="flat",
        )
        self.close_button.pack(padx=10, pady=(0, 10))  # Pack close button with padding

    # Method to update the label text
    def updateContent(self, text):
        self.label.config(text=text)

    # Showing the card over the parent window
    def show(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        # Bring the card on top of the parent
        self.lift()

    # Hide the card, removing it from the view
    def hide(self):
        self.place_forget()
