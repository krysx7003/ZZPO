import tkinter as tk
import ctypes as ct
import sys

def dark_title_bar(window):
    # Applying dark mode style on Windows
    if sys.platform == "win32":
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = 2
        value = ct.c_int(value)
        hwnd = ct.windll.user32.GetParent(window.winfo_id())
        ct.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ct.byref(value), ct.sizeof(value)
        )

root = tk.Tk()

# App title
root.title('ZZPOpuszczanieKrwi')

# Force window size to 800x800
root.geometry('400x400')

# Prevent resizing of the window
root.resizable(width=False, height=False)

# Apply dark title bar only on Windows
dark_title_bar(root)

# Set dark background for the root window (works on all platforms)
root.configure(bg='#121212')

# Example label with dark background and light text
label = tk.Label(root, text='Dark Background Example', bg='#121212', fg='white')
label.pack(pady=20)

root.mainloop()
