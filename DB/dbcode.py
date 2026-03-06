import sqlite3

database = "databaseforeksamenstuffplzgodholpimtrapedinthishellhole.db"

def add_character_and_initiative(character_name, initiative):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO characters (name, initiative) values (?, ?)", (character_name, initiative))
        conn.commit()

#with sqlite3.connect( <name of bd in her> ) as conn:

#cursor = conn.cursor()

#cursor.execute(INSERT INTO table_name(c1, c2 ) VALUES (?, ?))



