import sys  #from standard library, which provides direct access to variables and functions related to the interpreter and the execution of the program
import os   #interact with the operating system – for example, to manage files, folders or environment variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #this line adds the parent folder of the current file to the module search path so that Python can search for imports there

import sqlite3  #import for database
from analysis import all_habits_same_periodicity, longest_series_given_habit, longest_series_all_habits #imports functions from modul analysis


DB_PATH = "data/test_data.db" #path to test database
USER_ID = 1  #user id set to 1

def test_all_habits_same_periodicity(monkeypatch):
    
    #test filtering habits by a given periodicity (mocked selection), a simulated version of a real user selection
    
    #monkeypatch is a helper object from pytest that is used in testing to overwrite (patch) attributes or functions at runtime, i.e. to temporarily replace them

    #this line replaces (via monkey patching) the function questionary.select with a dummy version that always returns the value "daily" in .ask(), useful, for example,
    #for automated tests without user interaction
    monkeypatch.setattr("questionary.select", lambda *a, **k: type('', (), {'ask': lambda self: "daily"})())

    #the function should execute without error
    all_habits_same_periodicity(USER_ID, DB_PATH)


def test_longest_series_given_habit(monkeypatch):
    
    #test longest streak for a selected habit (mocked selection)
    

    #get one habit for mocking
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT habit_name, periodicity FROM habits WHERE user_id = ?", (USER_ID,))
    name, periodicity = cur.fetchone()
    con.close()

    #Mock the habit selection
    #It replaces questionary.select with a dummy function whose .ask() call always returns the string "{name} ({periodicity})" 
    #typically for tests to simulate a user choice
    #lamda: is an anonymous function (i.e. without def)
    # *a: collects any number of positional arguments into a tuple
    # **k: collects any number of named arguments (keyword args) into a dictionary
    #type: creates type(obj) the type of an object
    #setattr dynamically sets an attribute to an object, for example, a method or function
    monkeypatch.setattr("questionary.select", lambda *a, **k: type('', (), {'ask': lambda self: f"{name} ({periodicity})"})())

    #the function should execute without error
    longest_series_given_habit(USER_ID, DB_PATH)


def test_longest_series_all_habits():
    
    #test computing the longest streak of all habits
    
    #function should execute and show the longest streak
    longest_series_all_habits(USER_ID, DB_PATH)
