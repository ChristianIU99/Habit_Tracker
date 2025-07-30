import sqlite3  #for database
import pytest   #import pytest for unittest
from datetime import datetime #for date and time
from habit import Habit  #import class Habit of modul habit

#test database with user id set to 1
TEST_DB = "data/test_data.db"
TEST_USER_ID = 1


#gets last habit of database
def get_last_habit(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM habits ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    con.close()
    return result


def test_create_habit():
    
    #test setup for insert into database
    db_path = TEST_DB
    user_id = TEST_USER_ID
    habit_name = "Test Habit"
    description = "Test Description"
    periodicity = "daily"
    creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #insert directly by simulating interactive=False
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO habits (user_id, habit_name, description, periodicity, creation_datetime)
        VALUES (?, ?, ?, ?, ?)""",
        (user_id, habit_name, description, periodicity, creation_datetime))
    con.commit()
    con.close()

    #is used to validate (test/check) whether a saved entry has landed correctly in the database
    #assert is a statement, used in Python to check assumptions (assertions) in the code, things that must be true for the program to function correctly
    last_habit = get_last_habit(db_path)
    assert last_habit[1] == user_id
    assert last_habit[2] == habit_name
    assert last_habit[3] == description
    assert last_habit[4] == periodicity


def test_delete_habit():

    #setup: add a habit to delete
    #inserts a new record into the habits table of an SQLite database
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("INSERT INTO habits (user_id, habit_name, description, periodicity, creation_datetime) VALUES (?, ?, ?, ?, ?)",
                (TEST_USER_ID, "Delete Me", "desc", "daily", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    habit_id = cur.lastrowid
    con.commit()
    con.close()

    #delete the habit manually (simulate method call)
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("DELETE FROM habits WHERE id = ? AND user_id = ?", (habit_id, TEST_USER_ID))
    con.commit()
    con.close()

    #validate deletion
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
    habit = cur.fetchone()
    con.close()
    assert habit is None #assert is a statement, used in Python to check assumptions (assertions) in the code, things that must be true for the program to function correctly


def test_complete_habit():

    #setup: Insert a habit
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("INSERT INTO habits (user_id, habit_name, description, periodicity, creation_datetime) VALUES (?, ?, ?, ?, ?)",
                (TEST_USER_ID, "Completable Habit", "desc", "daily", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) #a tuple of values that is passed to the SQL query
    habit_id = cur.lastrowid
    con.commit()
    con.close()

    #simulate checkoff
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO checkoffs (habit_id, checkoff_time) VALUES (?, ?)", (habit_id, now))
    con.commit()

    #validate checkoff
    cur.execute("SELECT * FROM checkoffs WHERE habit_id = ?", (habit_id,))
    result = cur.fetchone()
    con.close()
    assert result is not None
