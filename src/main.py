"""
Main entry point for the blood donation management application.

This script initializes and runs the main application window,
starting the GUI event loop for user interaction.
"""

from src.frontEnd.App import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
