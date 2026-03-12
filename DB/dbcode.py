import sqlite3

DB = "databaseforeksamenstuffplzgodholpimtrapedinthishellhole.db"

def add_character_and_initiative(character_name, initiative):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO characters (name, initiative) values (?, ?)", (character_name, initiative))
        conn.commit()
    
def delete_character(character_name):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM characters WHERE name = ?", (character_name,))
        conn.commit()


#with sqlite3.connect( <name of bd in her> ) as conn:

#cursor = conn.cursor()

#cursor.execute(INSERT INTO table_name(c1, c2 ) VALUES (?, ?))