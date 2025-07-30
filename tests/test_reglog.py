import sqlite3  #import database
import pytest   #import pytest for unittest
import habit    #import modul habit
from hashlib import sha256  #for hashing password
from reglog import register, login  #import function register and login from modul reglog

TEST_DB = "data/test_data.db" #test database

#function for hashing password and convert into readable form
def hash_password(password):
    return sha256(password.encode()).hexdigest()


#function for cleaning database 
def clear_users_table():
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("DELETE FROM users")
    con.commit()
    con.close()


def test_register_new_user(monkeypatch):
    clear_users_table()
    
    #simulate user input (username, password)
    monkeypatch.setattr("questionary.text", lambda msg: type("Mock", (), {"ask": lambda: "testuser"}))
    monkeypatch.setattr("questionary.password", lambda msg: type("Mock", (), {"ask": lambda: "testpass"}))

    #dummy class for users with save
    import user
    class MockUser:
        def __init__(self, username, pw):
            self.username = username
            self.password = pw

        def store_user_in_db(self):
            con = sqlite3.connect(TEST_DB)
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
            con.commit()
            cur.execute("SELECT id FROM users WHERE username = ?", (self.username,))
            user_id = cur.fetchone()[0]
            con.close()
            return user_id

    user.User = MockUser #assigns the class or instance MockUser to the attribute User in the module or object user

    
    habit.Habit.create_default_habits = lambda *args, **kwargs: None  #overrides (mocks) the method create_default_habits of the class Habit in the module habit

    #registers a (test) user and ensures that the returned username is "testuser", a simple test to see if the registration is working correctly
    user_id, username = register("unused", "unused", TEST_DB)
    assert username == "testuser"

    #check if user was saved correctly
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
    user_data = cur.fetchone()
    con.close()
    assert user_data is not None
    assert user_data[1] == "testuser"



def test_login_success(monkeypatch):

    #cleaning the database
    clear_users_table()

    #parameter for database
    username = "testuser"
    password = "secret"
    hashed_pw = hash_password(password)

    #insert user into database
    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    con.commit()
    con.close()

    #simulate user query
    monkeypatch.setattr("questionary.text", lambda msg: type("Mock", (), {"ask": lambda: username}))
    monkeypatch.setattr("questionary.password", lambda msg: type("Mock", (), {"ask": lambda: password}))

    #the code tests whether the login returns the expected values — correct username and a valid user ID
    user_id, returned_username = login("unused", "unused", TEST_DB)
    assert returned_username == username
    assert isinstance(user_id, int)


def test_login_fail(monkeypatch):
    clear_users_table()

    #user not present
    #simulate user input (username and password) without anyone actually entering anything
    monkeypatch.setattr("questionary.text", lambda msg: type("Mock", (), {"ask": lambda: "wronguser"}))
    monkeypatch.setattr("questionary.password", lambda msg: type("Mock", (), {"ask": lambda: "wrongpass"}))

    #ensures that an incorrect login is correctly signaled with None, i.e. no successful user is logged in
    result = login("unused", "unused", TEST_DB)
    assert result is None

