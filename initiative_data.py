"""
Data Classes for D&D Initiative Tracker
Contains the core data models: Character and InitiativeTracker.
"""

class Character:
    """Represents a character or enemy in the initiative tracker."""
    
    def __init__(self, name, initiative):
        """
        Initialize a character.
        
        Args:
            name (str): The name of the character
            initiative (int): The initiative value (higher = goes first)
        """
        self.name = name
        self.initiative = initiative
    
    def __str__(self):
        """Return a formatted string for display."""
        return f"{self.name} (Initiative: {self.initiative})"


class InitiativeTracker:
    """Manages the list of characters and their order."""
    
    def __init__(self):
        """Initialize an empty character list."""
        self.characters = []
    
    def add_character(self, character):
        """
        Add a character to the tracker.
        
        Args:
            character (Character): The character to add
        """
        self.characters.append(character)
        self.sort_by_initiative()
    
    def remove_character(self, index):
        """
        Remove a character by their position in the list.
        
        Args:
            index (int): Position in the character list
        """
        if 0 <= index < len(self.characters):
            self.characters.pop(index)
    
    def sort_by_initiative(self):
        """Sort characters by initiative (highest first)."""
        self.characters.sort(key=lambda c: c.initiative, reverse=True)
    
    def get_characters(self):
        """Return the list of characters."""
        return self.characters