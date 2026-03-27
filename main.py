"""
D&D Initiative Tracker
"""

import tkinter as tk
from initiative_data import InitiativeTracker
from GUI.guipycode import MainWindow
from DB.dbcode import init_db


def main():
    # starter databasen
    init_db()
    
    # gør klar til at vise GUI'en
    root = tk.Tk()
    
    # opret en tracker og giv den til GUI'en
    tracker = InitiativeTracker()
    
    # opret GUI'en og giv den root og tracker
    app = MainWindow(root, tracker)
    
    # start programmet
    root.mainloop()


if __name__ == "__main__":
    main()
