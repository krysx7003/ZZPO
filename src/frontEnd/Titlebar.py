import ctypes as ct
import sys


def darkTitleBar(window):
    """
    Applies a dark title bar to a Tkinter window on Windows if Windows dark theme is enabled.

    This function modifies the window attributes to enable the system's dark mode
    for the title bar and window frame, using the Windows Desktop Window Manager (DWM) API.

    :param window: The Tkinter window (Tk or Toplevel instance) to modify.
    """

    if sys.platform == "win32":
        # Ensure the window is fully initialized and has a valid handle
        window.update()

        # Constant for enabling dark mode attribute in DWM (Desktop Window Manager)
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        # Value 2 enables immersive dark mode (windows API related value)
        value = 2
        # Convert Python int to C integer for API call
        value = ct.c_int(value)

        # Get the native window handle (HWND) of the Tkinter window's parent
        hwnd = ct.windll.user32.GetParent(window.winfo_id())

        # Call the DwmSetWindowAttribute function from dwmapi.dll to set the dark mode attribute
        ct.windll.dwmapi.DwmSetWindowAttribute(
            # Window handle
            hwnd,
            # Attribute to set
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            # Pointer to the value to set
            ct.byref(value),
            # Size of the value in bytes
            ct.sizeof(value),
        )
