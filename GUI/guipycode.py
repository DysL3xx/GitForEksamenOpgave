# GUI file through python

import tkinter as tk
from tkinter import ttk, messagebox

# Import the data classes from the data module
from initiative_data import Character, InitiativeTracker


class MainWindow:
    """The main Tkinter window for the initiative tracker."""

    def __init__(self, root, tracker):
        """
        Initialize the main window.

        Args:
            root (tk.Tk): The root Tkinter window
            tracker (InitiativeTracker): The initiative tracker instance
        """
        self.root = root
        self.root.title("D&D Initiative Tracker")
        self.root.geometry("500x600")

        # Use the provided tracker
        self.tracker = tracker

        # Build the UI
        self.setup_ui()

    def setup_ui(self):
        """Set up all the UI elements."""

        # Title Label
        title_label = ttk.Label(
            self.root,
            text="Initiative Tracker",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Input Frame - for adding characters
        input_frame = ttk.LabelFrame(
            self.root,
            text="Add Character",
            padding=10
        )
        input_frame.pack(fill="x", padx=10, pady=5)

        # Name input
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5)

        # Initiative input
        ttk.Label(input_frame, text="Initiative:").grid(row=1, column=0, sticky="w", pady=5)
        self.initiative_entry = ttk.Entry(input_frame, width=30)
        self.initiative_entry.grid(row=1, column=1, padx=5)

        # Type selection - Combobox
        ttk.Label(input_frame, text="Type:").grid(row=2, column=0, sticky="w", pady=5)
        self.type_combobox = ttk.Combobox(
            input_frame, 
            values=["hero", "ally", "enemy"],
            state="readonly",
            width=27
        )
        self.type_combobox.current(0)  # Default to "hero"
        self.type_combobox.grid(row=2, column=1, padx=5)
        
        # Add button
        add_button = ttk.Button(
            input_frame,
            text="Add Character",
            command=self.add_character
        )
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # next button
        next_button = ttk.Button(
            input_frame,
            text="next turn",
            command=self.next_turn
        )
        next_button.grid(row=3, column=2, columnspan=2, pady=10, padx=5)

        # previous button
        previous_button = ttk.Button(
            input_frame,
            text="previous turn",
            command=self.previous_turn
        )
        previous_button.grid(row=3, column=4, columnspan=2, pady=10, padx=5)

        # Character List Frame
        list_frame = ttk.LabelFrame(
            self.root,
            text="Turn Order",
            padding=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Listbox for displaying characters
        self.character_listbox = tk.Listbox(
            list_frame,
            height=12,
            font=("Arial", 11)
        )
        self.character_listbox.pack(fill="both", expand=True)

        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.character_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.character_listbox.config(yscrollcommand=scrollbar.set)

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Remove button
        remove_button = ttk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_character
        )
        remove_button.pack(side="left", padx=5)

        # Clear all button
        clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all
        )
        clear_button.pack(side="left", padx=5)

    def add_character(self):
        """Add a character to the tracker from the input fields."""
        name = self.name_entry.get().strip()
        initiative_str = self.initiative_entry.get().strip()
        char_type = self.type_combobox.get()

        # Validation
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a character name.")
            return

        if not initiative_str:
            messagebox.showwarning("Missing Initiative", "Please enter an initiative value.")
            return

        try:
            initiative = int(initiative_str)
        except ValueError:
            messagebox.showerror("Invalid Initiative", "Initiative must be a number.")
            return

        # Create and add character
        character = Character(name, initiative, char_type)
        self.tracker.add_character(character)

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.initiative_entry.delete(0, tk.END)
        self.type_combobox.current(0)  # Reset to default

        # Update display
        self.update_character_list()

    def next_turn(self):
            #Ryk den første karakter i listen til bunden og opdater
        characters = self.tracker.get_characters()
        if characters:
            first_character = characters.pop(0)
            characters.append(first_character)
            self.update_character_list()
        else:
            messagebox.showinfo("No Characters", "There are no characters in the tracker.")

    def previous_turn(self):
        #Ryk den bagerste krakter forrest i listen og opdater
        characters = self.tracker.get_characters()
        if characters:
            last_character = characters.pop()
            characters.insert(0, last_character)
            self.update_character_list()
        else:
            messagebox.showinfo("No Characters", "There are no characters in the tracker.")

    def remove_character(self):
        """Remove the selected character from the tracker."""
        selection = self.character_listbox.curselection()

        if not selection:
            messagebox.showwarning("No Selection", "Please select a character to remove.")
            return

        index = selection[0]
        self.tracker.remove_character(index)
        self.update_character_list()

    def clear_all(self):
        """Remove all characters (with confirmation)."""
        if not self.tracker.get_characters():
            messagebox.showinfo("Empty", "The tracker is already empty.")
            return

        if messagebox.askyesno("Clear All", "Remove all characters?"):
            self.tracker.characters = []
            self.update_character_list()

    def update_character_list(self):
        """Refresh the character list display."""
        self.character_listbox.delete(0, tk.END)

        for i, character in enumerate(self.tracker.get_characters()):
            self.character_listbox.insert(tk.END, str(character))
            # Set background color based on character type
            self.character_listbox.itemconfig(i, bg=character.get_display_color())