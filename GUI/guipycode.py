import tkinter as tk
from tkinter import ttk, messagebox
from initiative_data import Character, InitiativeTracker


# ============================================================================
# COLOR SCHEME - Fantasy-themed colors for D&D
# ============================================================================

BG_COLOR = "#1b1b1b"           # Deep charcoal background
PARCHMENT = "#2a2a2a"          # Dark card base
ACCENT = "#d4af37"             # Metallic gold for buttons
TEXT_LIGHT = "#f5eec7"         # Warm light text
TEXT_DARK = "#d6cfa3"          # Secondary text color

# Character type colors
HERO_COLOR = "#90EE90"         # Light green
ALLY_COLOR = "#6495ED"         # Cornflower blue
ENEMY_COLOR = "#FF7F50"        # Coral


# ============================================================================
# HELPER FUNCTION
# ============================================================================

def get_color_for_character_type(char_type):
    """
    Get the display color for a character based on their type.
    
    Args:
        char_type (str): "hero", "ally", or "enemy"
    
    Returns:
        str: Color code (hex format)
    """
    colors = {
        "hero": HERO_COLOR,
        "ally": ALLY_COLOR,
        "enemy": ENEMY_COLOR
    }
    return colors.get(char_type, "#FFFFFF")


# ============================================================================
# MAIN WINDOW CLASS
# ============================================================================

class MainWindow:
    """
    The main window for the D&D Initiative Tracker.
    
    This class:
    - Creates all the GUI elements (buttons, text fields, lists)
    - Handles what happens when users interact with the GUI
    - Updates the display when data changes
    - Communicates with the InitiativeTracker class
    """
    
    def __init__(self, root, tracker):
        """
        Initialize the main window.
        
        Args:
            root (tk.Tk): The root Tkinter window
            tracker (InitiativeTracker): The character tracker
        """
        self.root = root
        self.root.title("D&D Initiative Tracker")
        self.root.geometry("600x700")
        
        # Store the tracker so we can access it later
        self.tracker = tracker
        
        # Create all the GUI elements
        self.setup_ui()
        
        # Show the initial list of characters
        self.update_character_list()
    
    def setup_ui(self):
        """
        Set up all the UI elements.
        
        This creates:
        - The window styling and colors
        - The title label
        - The input section (for adding characters)
        - The turn order list
        - The action buttons
        """
        # Set the background color of the window
        self.root.configure(bg=BG_COLOR)
        
        # Configure the style for ttk widgets (themed widgets)
        self._configure_styles()
        
        # Create each section of the interface
        self._create_title_section()
        self._create_input_section()
        self._create_turn_controls_section()
        self._create_character_list_section()
        self._create_button_section()
    
    def _configure_styles(self):
        """Configure the colors and appearance of ttk widgets."""
        style = ttk.Style(self.root)
        style.theme_use('default')
        
        # Labels and frames
        style.configure('TLabel', background=PARCHMENT, foreground=TEXT_LIGHT)
        style.configure('TLabelframe', background=PARCHMENT, foreground=TEXT_LIGHT)
        style.configure('TLabelframe.Label', background=PARCHMENT, foreground=TEXT_LIGHT)
        style.configure('Parchment.TFrame', background=PARCHMENT)
        
        # Entry fields (text boxes)
        style.configure('TEntry', fieldbackground=PARCHMENT, foreground=TEXT_LIGHT)
        
        # Buttons
        style.configure('TButton', background=ACCENT, foreground=BG_COLOR)
        style.map('TButton', background=[('active', TEXT_DARK)])
        
        # Dropdown (combobox)
        style.configure('TCombobox', fieldbackground=PARCHMENT, background=PARCHMENT, foreground=TEXT_LIGHT)
        style.map('TCombobox', fieldbackground=[('readonly', PARCHMENT)])
    
    def _create_title_section(self):
        """Create the title label at the top."""
        title_label = ttk.Label(
            self.root,
            text="D&D Initiative Tracker",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
    
    def _create_input_section(self):
        """Create the section where users add new characters."""
        input_frame = ttk.LabelFrame(
            self.root,
            text="Add Character",
            padding=10
        )
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Character name input
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Initiative input
        ttk.Label(input_frame, text="Initiative:").grid(row=1, column=0, sticky="w", pady=5)
        self.initiative_entry = ttk.Entry(input_frame, width=30)
        self.initiative_entry.grid(row=1, column=1, padx=5, sticky="ew")
        
        # Character type dropdown
        ttk.Label(input_frame, text="Type:").grid(row=2, column=0, sticky="w", pady=5)
        self.type_combobox = ttk.Combobox(
            input_frame,
            values=["hero", "ally", "enemy"],
            state="readonly",
            width=27
        )
        self.type_combobox.current(0)  # Default to "hero"
        self.type_combobox.grid(row=2, column=1, padx=5, sticky="ew")
        
        # Add button
        add_button = ttk.Button(
            input_frame,
            text="Add Character",
            command=self._on_add_character
        )
        add_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        input_frame.columnconfigure(1, weight=1)
    
    def _create_turn_controls_section(self):
        """Create the buttons to navigate through turns."""
        turn_frame = ttk.Frame(self.root)
        turn_frame.pack(fill="x", padx=10, pady=5)
        
        # Previous turn button
        previous_button = ttk.Button(
            turn_frame,
            text="← Previous Turn",
            command=self._on_previous_turn
        )
        previous_button.pack(side="left", padx=5, expand=True, fill="x")
        
        # Current turn display
        self.turn_label = ttk.Label(
            turn_frame,
            text="No characters yet",
            font=("Arial", 10, "bold")
        )
        self.turn_label.pack(side="left", padx=5, expand=True)
        
        # Next turn button
        next_button = ttk.Button(
            turn_frame,
            text="Next Turn →",
            command=self._on_next_turn
        )
        next_button.pack(side="left", padx=5, expand=True, fill="x")
    
    def _create_character_list_section(self):
        """Create the section that displays the list of characters."""
        list_frame = ttk.LabelFrame(
            self.root,
            text="Turn Order (Highest Initiative First)",
            padding=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create the listbox
        self.character_listbox = tk.Listbox(
            list_frame,
            height=14,
            font=("Arial", 11),
            bg=PARCHMENT,
            fg=TEXT_LIGHT,
            selectbackground=ACCENT,
            selectforeground=BG_COLOR,
            activestyle="none"
        )
        self.character_listbox.pack(fill="both", expand=True, side="left")
        
        # Create and attach a scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.character_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.character_listbox.config(yscrollcommand=scrollbar.set)
    
    def _create_button_section(self):
        """Create the action buttons (Remove, Clear All)."""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Remove button
        remove_button = ttk.Button(
            button_frame,
            text="Remove Selected",
            command=self._on_remove_character
        )
        remove_button.pack(side="left", padx=5, expand=True, fill="x")
        
        # Clear all button
        clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self._on_clear_all
        )
        clear_button.pack(side="left", padx=5, expand=True, fill="x")
    
    # ========================================================================
    # EVENT HANDLERS - These methods are called when users click buttons
    # ========================================================================
    
    def _on_add_character(self):
        """Handle the 'Add Character' button click."""
        # Get the values from the input fields
        name = self.name_entry.get().strip()
        initiative_str = self.initiative_entry.get().strip()
        char_type = self.type_combobox.get()
        
        # Validate that name is not empty
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a character name.")
            return
        
        # Validate that initiative is not empty
        if not initiative_str:
            messagebox.showwarning("Missing Initiative", "Please enter an initiative value.")
            return
        
        # Validate that initiative is a number
        try:
            initiative = int(initiative_str)
        except ValueError:
            messagebox.showerror("Invalid Initiative", "Initiative must be a whole number.")
            return
        
        # Try to add the character using the tracker
        success = self.tracker.add_character(name, initiative, char_type)
        
        if success:
            # Clear the input fields
            self.name_entry.delete(0, tk.END)
            self.initiative_entry.delete(0, tk.END)
            self.type_combobox.current(0)
            
            # Update the display
            self.update_character_list()
        else:
            messagebox.showerror("Error", f"A character named '{name}' already exists.")
    
    def _on_next_turn(self):
        """Handle the 'Next Turn' button click."""
        characters = self.tracker.get_characters()
        
        
        current = self.tracker.get_current_character()
        self.tracker.next_turn()
        next_char = self.tracker.get_current_character()
        
        
        self.update_character_list()
    
    def _on_previous_turn(self):
        """Handle the 'Previous Turn' button click."""
        characters = self.tracker.get_characters()
        
        
        self.tracker.previous_turn()
        current = self.tracker.get_current_character()
        
        self.update_character_list()
    
    def _on_remove_character(self):
        """Handle the 'Remove Selected' button click."""
        # Get which character is selected in the listbox
        selection = self.character_listbox.curselection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a character to remove.")
            return
        
        # Get the selected character
        index = selection[0]
        character = self.tracker.get_characters()[index]
        
        # Ask for confirmation
        if messagebox.askyesno("Confirm Removal", f"Remove '{character.name}' from the tracker?"):
            self.tracker.remove_character(index)
            self.update_character_list()
            messagebox.showinfo("Removed", f"'{character.name}' has been removed.")
    
    def _on_clear_all(self):
        """Handle the 'Clear All' button click."""
        characters = self.tracker.get_characters()
        
        if not characters:
            messagebox.showinfo("Empty", "The tracker is already empty.")
            return
        
        # Ask for confirmation
        if messagebox.askyesno("Clear All", "Remove all characters?\n\nThis cannot be undone!"):
            self.tracker.clear_all()
            self.update_character_list()
            messagebox.showinfo("Cleared", "All characters have been removed.")
    
    # ========================================================================
    # DISPLAY REFRESH - Updates what the user sees on screen
    # ========================================================================
    
    def update_character_list(self):
        """
        Update the character list display.
        
        This is called whenever characters change.
        It reads from the tracker and updates what the user sees.
        """
        # Clear the current display
        self.character_listbox.delete(0, tk.END)
        
        # Get the current characters
        characters = self.tracker.get_characters()
        
        # Add each character to the display
        for i, character in enumerate(characters):
            # Create the display text
            display_text = str(character)
            
            # Add it to the listbox
            self.character_listbox.insert(tk.END, display_text)
            
            # Color it based on character type
            color = get_color_for_character_type(character.char_type)
            self.character_listbox.itemconfig(i, bg=color)
        
        # Update the turn label
        self._update_turn_label()
    
    def _update_turn_label(self):
        """Update the label showing whose turn it is."""
        current = self.tracker.get_current_character()
        characters = self.tracker.get_characters()
        
        if not characters:
            self.turn_label.config(text="No characters yet")
        else:
            turn_number = self.tracker.current_turn_index + 1
            total = len(characters)
            text = f"Turn {turn_number}/{total}: {current.name}'s turn"
            self.turn_label.config(text=text)
