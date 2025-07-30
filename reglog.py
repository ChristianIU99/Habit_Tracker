from os.path import join, abspath, dirname
from db import db_path      #imports parameter db_path from modul db.py
from habit import Habit     #imports class "Habit" from modul habit.py
import questionary          #for menu selection
import sqlite3              #for the sqlite database
import click                #for Command Line Interface (CLI)
import hashlib              #sufficient for this application, otherwise bcrypt is even more secure
import user                 #imports modul user for using class user with their methods



#function register to register a new user
def register(username, password):
    
    click.echo("*****Registration*****")  #text on command line

    # loop to repeat the function if something goes wrong
    while True:

        #Enter username and password, which are stored in the assigned variables
        username = questionary.text("Username:").ask()
        password = questionary.password("Password:").ask()
    
         
        con = sqlite3.connect(db_path) #connection to initialized database
        cur = con.cursor() #creates a cursor object that is necessary to execute SQL commands with a database connection


        cur.execute("SELECT * FROM users WHERE username = ?", (username,)) #here a query is sent to the database to search for a user with a specific username
        if cur.fetchone(): #returns the current line from users
            click.echo("Username already exists! \nChoose another username!") #error message command line
            con.close() #close connection to database
            continue #loop is repeated
        else:
            hashed_pw = hash_password(password) #function hash_password converts password
            new_user = user.User(username, hashed_pw) #new object of class User
            user_id = new_user.store_user_in_db() #user data stores in database
            
            Habit.create_default_habits(user_id, db_path, username) #method of class Habit which creates default habits for the new user
            
            con.commit() #save changes
            con.close() #close connection to database
            click.echo("Registration successful!") #text on CLI
            break #finish loop
        
    click.echo("You will be logged in automatically!") #text on CLI
    return (user_id, username) #function register returns username and user_id for the next functions



#funtion for login
def login(username, password):
    click.echo("*****Login*****")

    while True:

        #enter username and password
        username = questionary.text("Benutzername:").ask()
        password = questionary.password("Passwort:").ask()

        #connection to database
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        #checks whether the username already exists or not
        cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        con.close()

        #If the name does not exist you return to the login/register menu
        if not result:
            click.echo("User does not exist yet. Please register first!\n")
            return None

        #password get hashed for comparison
        pw = hash_password(password)
        user_id = result[0]  #assigns the first position of the tuple (id, password) to the variable = id
        stored_password = result[1] #assigns the second position of the tuple (id, password) to the variable = hashed password

        if result and stored_password == pw: #comparison between result, stored_password and pw
            click.echo(f"Welcome back, {username}!")  #welcomes users  
            return user_id, username   #funtion returns user_id und username for main menu  
        else:
            click.echo("Incorrect username or password. Please try again! \n") #repeats login
        


#function for password hash, protects password
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest() #sha256 = cryptographic hash algorithm, fixed 256-bit value; hexdigest() = converts binary hash to hexadecimal = readable

