import tkinter as tk
import sys
import os

# Ensure the root folder is on the python search path so imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import the GUI
from gui import ScientificDataApp

def main():
    root = tk.Tk()
    
    # Optional styling for window icon/scaling if supported
    try:
        # On Windows, this enhances DPI awareness so the text looks crisp
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
        
    app = ScientificDataApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
