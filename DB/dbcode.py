import sqlite3

DB = "databaseforeksamenstuffplzgodhelpimtrapedinthishellhole.db"

def init_db():
    """
    Initialize the database by creating the table if it doesn't exist.
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS initiativefordnd (
                name TEXT PRIMARY KEY,
                initiative TEXT,
                status TEXT,
                pic TEXT
            )""")
    except Exception as error:
        print(f"Error initializing database: {error}")

def add_character(name, initiative, status, pic):
    """
    Add a new character to the database.
    
    Args:
        name (str): Character name
        initiative (int): Initiative value (higher = acts first)
        status (str): Character type ("hero", "ally", or "enemy")
        pic (str): Picture path (optional)
    
    Returns:
        bool: True if successful, False if it fails
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO initiativefordnd (name, initiative, status, pic) VALUES (?, ?, ?, ?)",
                (name, str(initiative), status, pic)
            )
            conn.commit()
        return True
    except Exception as error:
        print(f"Error adding character: {error}")
        return False


def delete_character(name):
    """
    Delete a character from the database.
    
    Args:
        name (str): The name of the character to delete
    
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM initiativefordnd WHERE name = ?", (name,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as error:
        print(f"Error deleting character: {error}")
        return False


def update_initiative(name, initiative):
    """
    Update a character's initiative value.
    
    Args:
        name (str): The character's name
        initiative (int): The new initiative value
    
    Returns:
        bool: True if updated successfully, False otherwise
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE initiativefordnd SET initiative = ? WHERE name = ?",
                (str(initiative), name)
            )
            conn.commit()
            return cursor.rowcount > 0
    except Exception as error:
        print(f"Error updating initiative: {error}")
        return False


def del_all_characters():
    """
    Delete all characters from the database.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM initiativefordnd")
            conn.commit()
        return True
    except Exception as error:
        print(f"Error deleting all characters: {error}")
        return False


def get_all_characters():
    """
    Get all characters from the database.
    Characters are sorted by initiative (highest first).
    
    Returns:
        list: List of tuples (name, initiative, status, pic)
              Returns empty list if no characters or error occurs
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute("""CREATE TABLE IF NOT EXISTS initiativefordnd (
                name TEXT PRIMARY KEY,
                initiative TEXT,
                status TEXT,
                pic TEXT
            )""")
            # ORDER BY CAST converts text to number for proper sorting
            cursor.execute(
                "SELECT name, initiative, status, pic FROM initiativefordnd ORDER BY CAST(initiative AS INTEGER) DESC"
            )
            results = cursor.fetchall()
            # Convert initiative from text to integer for easier use
            return [(name, int(initiative), status, pic) for name, initiative, status, pic in results]
    except Exception as error:
        print(f"Error retrieving characters: {error}")
        return []


def get_character(name):
    """
    Get a specific character by name.
    
    Args:
        name (str): The character's name
    
    Returns:
        tuple: (name, initiative, status, pic) if found
               None if not found
    """
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, initiative, status, pic FROM initiativefordnd WHERE name = ?",
                (name,)
            )
            result = cursor.fetchone()
            if result:
                name, initiative, status, pic = result
                # Convert initiative to integer
                return (name, int(initiative), status, pic)
            return None
    except Exception as error:
        print(f"Error retrieving character: {error}")
        return None


def character_exists(name):
    """
    Check if a character with this name is already in the database.
    
    Args:
        name (str): The character's name
    
    Returns:
        bool: True if character exists, False otherwise
    """
    return get_character(name) is not None
