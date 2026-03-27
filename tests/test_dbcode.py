import os
import sqlite3
from DB import dbcode

TEST_DB = "tests/test_database.db"


def setup_module(module):
    # Brug separat tests DB-fil for ikke at påvirke produktions-data
    dbcode.DB = TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    dbcode.init_db()


import gc
import time


def teardown_module(module):
    if os.path.exists(TEST_DB):
        for _ in range(5):
            try:
                os.remove(TEST_DB)
                break
            except PermissionError:
                gc.collect()
                time.sleep(0.05)


def test_init_db_creates_table():
    assert os.path.exists(TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='initiativefordnd'")
    assert cur.fetchone() is not None
    conn.close()


def test_add_get_character():
    added = dbcode.add_character("TestHero", 15, "hero", "")
    assert added, "add_character skulle returnere True for en ny karakter"
    c = dbcode.get_character("TestHero")
    assert c is not None, "get_character skulle returnere en tuple for TestHero"
    assert c == ("TestHero", 15, "hero", ""), f"Karakterdata mismatch: {c}"


def test_update_initiative():
    updated = dbcode.update_initiative("TestHero", 18)
    assert updated, "update_initiative skulle returnere True når TestHero findes"
    c = dbcode.get_character("TestHero")
    assert c is not None, "Efter opdatering skal TestHero stadig findes"
    assert c[1] == 18, f"Initiative værdi skal være 18, fandt {c[1]}"


def test_character_exists():
    assert dbcode.character_exists("TestHero")
    assert not dbcode.character_exists("MissingOne")


def test_delete_character():
    deleted = dbcode.delete_character("TestHero")
    assert deleted
    assert dbcode.get_character("TestHero") is None


def test_del_all_characters():
    dbcode.add_character("A", 10, "ally", "")
    dbcode.add_character("B", 5, "enemy", "")
    assert len(dbcode.get_all_characters()) >= 2
    dbcode.del_all_characters()
    assert dbcode.get_all_characters() == []
