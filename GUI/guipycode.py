import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from initiative_data import Character, InitiativeTracker
from PIL import Image, ImageTk
import os


# Farver
BG_COLOR = "#1b1b1b"           # Deep charcoal background
PARCHMENT = "#2a2a2a"          # Dark card base
ACCENT = "#d4af37"             # Metallic gold for buttons
TEXT_LIGHT = "#f5eec7"         # Warm light text
TEXT_DARK = "#d6cfa3"          # Secondary text color

# karaktertype farver
HERO_COLOR = "#289928"         # Light green
ALLY_COLOR = "#6495ED"         # Cornflower blue
ENEMY_COLOR = "#FF7F50"        # Coral



# HELPER FUNKTION

def get_color_for_character_type(char_type):
    """
    henter farver baseret på karaktertype
    
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


# klasse for hovedvinduet

class MainWindow:
    """
    klasse for hovedvinduet i GUI'en
    """
    
    def __init__(self, root, tracker):
        """
        Initialiserer hovedvinduet og opretter alle GUI-elementer.
        Args:
            root (tk.Tk): The root Tkinter window
            tracker (InitiativeTracker): The character tracker
        """
        self.root = root
        self.root.title("D&D Initiative Tracker")
        self.root.geometry("600x700")
        
        # gem tracker
        self.tracker = tracker
        
        # gem billedsti
        self.selected_image_path = ""
        
        # opret GUI-elementerne
        self.setup_ui()
        
        # vis karaktererne i trackeren
        self.update_character_list()
    
    def setup_ui(self):
        """
        Opret og arranger alle GUI-elementer i vinduet.
        """
        # baggrund
        self.root.configure(bg=BG_COLOR)
        
        # konfigurer stilarter for ttk widgets
        self._configure_styles()
        
        # lav sektioner
        self._create_title_section()
        self._create_input_section()
        self._create_turn_controls_section()
        self._create_character_list_section()
        self._create_button_section()
    
    def _configure_styles(self):
        """farver og udseende"""
        style = ttk.Style(self.root)
        style.theme_use('default')
        
        # Labels
        style.configure('TLabel', background=PARCHMENT, foreground=TEXT_LIGHT)
        style.configure('TLabelframe', background=PARCHMENT, foreground=TEXT_LIGHT)
        style.configure('TLabelframe.Label', background=PARCHMENT, foreground=TEXT_LIGHT)
        style.configure('Parchment.TFrame', background=PARCHMENT)
        
        # textboxe
        style.configure('TEntry', fieldbackground=PARCHMENT, foreground=TEXT_LIGHT)
        
        # knapper
        style.configure('TButton', background=ACCENT, foreground=BG_COLOR)
        style.map('TButton', background=[('active', TEXT_DARK)])
        
        # Dropdown
        style.configure('TCombobox', fieldbackground=PARCHMENT, background=PARCHMENT, foreground=TEXT_LIGHT)
        style.map('TCombobox', fieldbackground=[('readonly', PARCHMENT)])
    
    def _create_title_section(self):
        """lav en titel for programmet"""
        title_label = ttk.Label(
            self.root,
            text="D&D Initiative Tracker",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
    
    def _create_input_section(self):
        """sektion til karakter input og billedvalg"""
        input_frame = ttk.LabelFrame(
            self.root,
            text="Add Character",
            padding=10
        )
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # karakter navn
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Initiative
        ttk.Label(input_frame, text="Initiative:").grid(row=1, column=0, sticky="w", pady=5)
        self.initiative_entry = ttk.Entry(input_frame, width=30)
        self.initiative_entry.grid(row=1, column=1, padx=5, sticky="ew")
        
        # karakter type
        ttk.Label(input_frame, text="Type:").grid(row=2, column=0, sticky="w", pady=5)
        self.type_combobox = ttk.Combobox(
            input_frame,
            values=["hero", "ally", "enemy"],
            state="readonly",
            width=27
        )
        self.type_combobox.current(0)  # Default to "hero"
        self.type_combobox.grid(row=2, column=1, padx=5, sticky="ew")
        
        # billedevalg
        ttk.Label(input_frame, text="Image:").grid(row=3, column=0, sticky="w", pady=5)
        self.image_path_label = ttk.Label(input_frame, text="No image selected", background=PARCHMENT, foreground=TEXT_LIGHT, relief="sunken")
        self.image_path_label.grid(row=3, column=1, padx=5, sticky="ew")
        select_image_button = ttk.Button(
            input_frame,
            text="Select Image",
            command=self._on_select_image
        )
        select_image_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        
        # knap til at tilføje karakteren
        add_button = ttk.Button(
            input_frame,
            text="Add Character",
            command=self._on_add_character
        )
        add_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        input_frame.columnconfigure(1, weight=1)
    
    def _on_select_image(self):
        """når man skal vælge billede til karakteren"""
        static_dir = os.path.join(os.getcwd(), "Statik")
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        file_path = filedialog.askopenfilename(
            initialdir=static_dir,
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            # gem billesti
            if file_path.startswith(static_dir):
                relative_path = os.path.relpath(file_path, os.getcwd())
                self.selected_image_path = relative_path
                self.image_path_label.config(text=os.path.basename(file_path))
            else:
                messagebox.showwarning("Invalid Location", "Please select an image from the Statik folder.")
                self.selected_image_path = ""
                self.image_path_label.config(text="No image selected")
        else:
            self.selected_image_path = ""
            self.image_path_label.config(text="No image selected")
    
    def _create_turn_controls_section(self):
        """knapperr til turer"""
        turn_frame = ttk.Frame(self.root)
        turn_frame.pack(fill="x", padx=10, pady=5)
        
        previous_button = ttk.Button(
            turn_frame,
            text="← Previous Turn",
            command=self._on_previous_turn
        )
        previous_button.pack(side="left", padx=5, expand=True, fill="x")
        
        # viser nuværende tur
        self.turn_label = ttk.Label(
            turn_frame,
            text="No characters yet",
            font=("Arial", 10, "bold")
        )
        self.turn_label.pack(side="left", padx=5, expand=True)
        
        next_button = ttk.Button(
            turn_frame,
            text="Next Turn →",
            command=self._on_next_turn
        )
        next_button.pack(side="left", padx=5, expand=True, fill="x")
    
    def _create_character_list_section(self):
        """karakterliste og scrollbar"""
        list_frame = ttk.LabelFrame(
            self.root,
            text="Turn Order (Highest Initiative First)",
            padding=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # laver listen
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
        
        # scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.character_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.character_listbox.config(yscrollcommand=scrollbar.set)
        
        # bviser billede
        self.preview_label = ttk.Label(list_frame, text="Select a character to view image", background=PARCHMENT, foreground=TEXT_LIGHT)
        self.preview_label.pack(fill="x", pady=5)
        self.character_listbox.bind("<<ListboxSelect>>", self._on_character_select)
    
    def _create_button_section(self):
        """laver knapper til at fjerne og rydde alle karakterer."""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        remove_button = ttk.Button(
            button_frame,
            text="Remove Selected",
            command=self._on_remove_character
        )
        remove_button.pack(side="left", padx=5, expand=True, fill="x")
        
        clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self._on_clear_all
        )
        clear_button.pack(side="left", padx=5, expand=True, fill="x")
    

    # EVENT HANDLERS 
    
    def _on_add_character(self):
        """tilføj karakter"""
        # henter givne værdier
        name = self.name_entry.get().strip()
        initiative_str = self.initiative_entry.get().strip()
        char_type = self.type_combobox.get()
        
        # tjekker om navn er givet
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a character name.")
            return
        
        # tjekker om initiative er givet
        if not initiative_str:
            messagebox.showwarning("Missing Initiative", "Please enter an initiative value.")
            return
        
        # tjekker om initiative er et heltal
        try:
            initiative = int(initiative_str)
        except ValueError:
            messagebox.showerror("Invalid Initiative", "Initiative must be a whole number.")
            return
        
        # tilføj karakteren til trackeren
        success = self.tracker.add_character(name, initiative, char_type)
        
        if success:
            # tømmer felter
            self.name_entry.delete(0, tk.END)
            self.initiative_entry.delete(0, tk.END)
            self.type_combobox.current(0)
            self.selected_image_path = ""
            self.image_path_label.config(text="No image selected")
            
            # opdaterer listen
            self.update_character_list()
        else:
            messagebox.showerror("Error", f"A character named '{name}' already exists.")
    
    def _on_next_turn(self):
        """næste tur knap"""
        characters = self.tracker.get_characters()
        
        
        current = self.tracker.get_current_character()
        self.tracker.next_turn()
        next_char = self.tracker.get_current_character()
        
        
        self.update_character_list()
    
    def _on_previous_turn(self):
        """sidste tur knap"""
        characters = self.tracker.get_characters()
        
        
        self.tracker.previous_turn()
        current = self.tracker.get_current_character()
        
        self.update_character_list()
    
    def _on_remove_character(self):
        """fjern valgte karakter"""
        selection = self.character_listbox.curselection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a character to remove.")
            return
        
        # find karakteren baseret på valgt index
        index = selection[0]
        character = self.tracker.get_characters()[index]
        
        # tjekker om brugeren vil fjerne karakteren
        if messagebox.askyesno("Confirm Removal", f"Remove '{character.name}' from the tracker?"):
            self.tracker.remove_character(index)
            self.update_character_list()
            messagebox.showinfo("Removed", f"'{character.name}' has been removed.")
    
    def _on_clear_all(self):
        """fjern alle karakterer"""
        characters = self.tracker.get_characters()
        
        if not characters:
            messagebox.showinfo("Empty", "The tracker is already empty.")
            return
        
        # tjekker om brugeren vil fjerne alle karakterer
        if messagebox.askyesno("Clear All", "Remove all characters?\n\nThis cannot be undone!"):
            self.tracker.clear_all()
            self.update_character_list()
            messagebox.showinfo("Cleared", "All characters have been removed.")
    
    
    # DISPLAY REFRESH: opdaterer det brugeren ser
    
    
    def update_character_list(self):
        """
        Opdaterer listen over karakterer i GUI'en baseret på trackeren.
        """
        # tømmer listen
        self.character_listbox.delete(0, tk.END)
        
        # henter karakterer fra trackeren
        characters = self.tracker.get_characters()
        
        # tilføjer karaktererne til listen
        for i, character in enumerate(characters):
            display_text = str(character)
            if character.pic_path:
                display_text += " [Image]"
            
            # indsætter i listboxen
            self.character_listbox.insert(tk.END, display_text)
            
            # farve
            color = get_color_for_character_type(character.char_type)
            self.character_listbox.itemconfig(i, bg=color)
        
        # opdaterer tur label
        self._update_turn_label()
    
    def _update_turn_label(self):
        """Opdaterer label der viser hvilken karakters tur det er."""
        current = self.tracker.get_current_character()
        characters = self.tracker.get_characters()
        
        if not characters:
            self.turn_label.config(text="No characters yet")
        else:
            turn_number = self.tracker.current_turn_index + 1
            total = len(characters)
            text = f"Turn {turn_number}/{total}: {current.name}'s turn"
            self.turn_label.config(text=text)

    def _on_character_select(self, event):
        """karakter valg"""
        sel = self.character_listbox.curselection()
        if not sel:
            return
        character = self.tracker.get_characters()[sel[0]]
        self._update_preview_label(character)

    def _update_preview_label(self, character):
        """viser billede"""
        if not character.pic_path:
            self.preview_label.config(text="No image for this character", image="")
            return
        try:
            full_path = os.path.join(os.getcwd(), character.pic_path)
            image = Image.open(full_path)
            image.thumbnail((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  
        except Exception as e:
            self.preview_label.config(text=f"Cannot load image: {str(e)}", image="")
