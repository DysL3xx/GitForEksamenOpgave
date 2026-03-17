from DB import dbcode as db


class Character:
    def __init__(self, name, initiative, char_type="hero"):
        self.name = name
        self.initiative = initiative
        self.char_type = char_type  # "hero", "ally", or "enemy"
    
    def __str__(self):
        return f"{self.name} (Initiative: {self.initiative}) - {self.char_type.title()}"
    
    def get_display_color(self):
        colors = {
            "hero": "#90EE90",    # Light green
            "ally": "#6495ED",    # Cornflower blue
            "enemy": "#FF7F50"    # Coral
        }
        return colors.get(self.char_type, "#FFFFFF")  # Default to white


class InitiativeTracker:

    def __init__(self):
        """Initialize the tracker and load characters from the database."""
        self.characters = []
        self.current_turn_index = 0
        
        # Load existing characters from database
        self._load_from_database()
    
    def _load_from_database(self):

        self.characters = []
        character_data = db.get_all_characters()
        
        for name, initiative, char_type, picture_path in character_data:
            character = Character(name, initiative, char_type)
            self.characters.append(character)
    
    def add_character(self, name, initiative, char_type="hero"):
        # Check if character already exists
        if db.character_exists(name):
            return False
        
        # Add to database
        success = db.add_character(name, initiative, char_type, "")
        
        if success:
            # Reload from database to stay in sync
            self._load_from_database()
            return True
        
        return False
    
    def remove_character(self, index):
        if 0 <= index < len(self.characters):
            character_to_remove = self.characters[index]
            db.delete_character(character_to_remove.name)
            # Reload from database to stay in sync
            self._load_from_database()
            return True
        
        return False
    
    def sort_by_initiative(self):
        self.characters.sort(key=lambda c: c.initiative, reverse=True)
    
    def get_characters(self):
        """
        Get the list of all characters.
        
        Returns:
            list: List of Character objects
        """
        return self.characters
    
    def get_current_character(self):
        """
        Get the character whose turn it is right now.
        
        Returns:
            Character: The current character, or None if no characters exist
        """
        if not self.characters:
            return None
        return self.characters[self.current_turn_index]
    
    def next_turn(self):
        """
        Move to the next character's turn.
        
        If we're at the end of the list, loop back to the beginning.
        """
        if self.characters:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.characters)
    
    def previous_turn(self):
        """
        Move to the previous character's turn.
        
        If we're at the beginning, loop back to the end.
        """
        if self.characters:
            self.current_turn_index = (self.current_turn_index - 1) % len(self.characters)
    
    def clear_all(self):
        """
        Remove all characters from the tracker and database.
        
        Returns:
            bool: True if successful
        """
        db.del_all_characters()
        self._load_from_database()
        self.current_turn_index = 0
        return True
