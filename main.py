"""
D&D Initiative Tracker - Main Application
This module runs the application by importing data classes and GUI components.
"""

import tkinter as tk
from initiative_data import InitiativeTracker
from GUI.guipycode import MainWindow
from DB.dbcode import init_db


def main():
    # Initialize the database
    init_db()
    
    # Create the root Tkinter window
    root = tk.Tk()
    
    # Create the tracker (this loads all characters from the database)
    tracker = InitiativeTracker()
    
    # Create the main GUI window
    app = MainWindow(root, tracker)
    
    # Start the event loop
    # The program will run here until the user closes the window
    root.mainloop()


if __name__ == "__main__":
    main()
