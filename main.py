"""
D&D Initiative Tracker - Main Application
This module runs the application by importing data classes and GUI components.
"""

import tkinter as tk

# Import data classes and GUI
from initiative_data import Character, InitiativeTracker
from GUI.gui import MainWindow


def main():
    """Run the application."""
    root = tk.Tk()
    tracker = InitiativeTracker()
    app = MainWindow(root, tracker)
    root.mainloop()


if __name__ == "__main__":
    main()
