import sqlite3

DB = "databaseforeksamenstuffplzgodholpimtrapedinthishellhole.db"

def add_character(name, initiative, status, pic):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO characters (name, initiative, status, pic) values (?, ?, ?, ?)", (name, initiative, status, pic))
        conn.commit()

def delete_character(name):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM characters WHERE name = ?", (name,))
        conn.commit()

def update_initiative(name, initiative):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE characters SET initiative = ? WHERE name = ?", (initiative, name))
        conn.commit()

def del_all_characters():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM characters")
        conn.commit()   