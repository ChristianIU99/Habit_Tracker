from datetime import datetime, timedelta #imports methods datetime and timedelta from library datetime
from db import db_path   #imports db_path from modul db
import questionary       #for menu selection
import sqlite3           #for sqlite3 database
import random            #for random predefined habits after registration
import click             #for Command Line Interface (CLI)
import json              #for saving the predefined habits in a json-file
import os                #interact with the operating system – for example, to manage files, folders or environment variables



#class "Habit" with the associated methods
class Habit:

    #The __init__ method in a class is the constructor — it is called automatically when a new object of the class is created
    #It is used to define initial values (attributes) for that object
    def __init__(self, id, user_id, habit_name, discription, periodicity, creation_datetime):
        self.id = id
        self.user_id = user_id
        self.habit_name = habit_name
        self.discription = discription
        self.periodicity = periodicity
        self.creation_datetime = creation_datetime



    #method for creating habits, user id comes from login
    def create_habit(user_id, db_path, interactive = True, habit_id = None):

        if interactive:
            habit_name = questionary.text("Name of Habit:").ask() #enter name of habit
            description = questionary.text("Description:").ask()  #enter description
            periodicity = questionary.select(
                    "What time frame should the habit be in?",    #choice between daily and weekly
                    choices = ["daily", "weekly"]
                ).ask()
        else:
            selected = habit_id
            
        #Gets the current date and time from the system
        #Formats the datetime object as a readable string in the desired format
        creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")       

        #connection to database
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("INSERT INTO habits(user_id, habit_name, description, periodicity, creation_datetime) VALUES(?, ?, ?, ?, ?)", 
                    (user_id, habit_name, description, periodicity, creation_datetime)) #insert the entered descriptions in the table 

        #ends connection to database
        con.commit()
        con.close()
        click.echo("Habit was saved!")



    #method to delete habits
    def delete_habit(user_id, db_path, interactive = True, habit_id = None):

        if interactive:
            #connection to database
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("SELECT id, habit_name FROM habits WHERE user_id = ?", (user_id,)) #gets habits out of table
            habits = cur.fetchall() #returns all habits assigned to the user to variable as a tuple
        else:
            selected = habit_id

        #checks if habits exist
        if not habits:
            click.echo("No habits available to delete!")
            con.close()
            return #ends method

        habit_choices = [f" {habit[0]} - {habit[1]}" for habit in habits]  #gets id and habit name from the previously created tuple and returns a tuple to variable  
        select = questionary.select(
                "Which habit do you want to delete?", #choice of what habit you want to delete
                choices = habit_choices
                ).ask()


        habit_id = int(select.split(" - ")[0])   #separates select at the sign - and gives habit_id the value at position 0 in this case the ID of the habit
        cur.execute("DELETE FROM habits WHERE id = ? AND user_id = ?", (habit_id, user_id,)) #deletes habits from table "habits"
        con.commit()
        con.close()
        click.echo("Habit deleted")
 


    #method to complete habits
    def complete_habit(user_id, db_path, interactive = True, habid_id = None):

        if interactive:
            #connection to database
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("SELECT id, habit_name, periodicity FROM habits WHERE user_id = ?", (user_id,)) #gets id, habit name and periodicity from table habits
            habits = cur.fetchall() #gets a tuple of it
        else:
            selected = habit_id

        #checks whether habits exist
        if not habits:
            click.echo("No habits to tick off.")
            con.close()
            return

        habit_choices = [f"{habit[0]} - {habit[1]} - {(habit[2])}" for habit in habits] #tuple of id, habit name and periodicity for choice
        selected = questionary.select("Which habit have you completed?", choices=habit_choices).ask() #choice which habit you want complete
        habit_id = int(selected.split(" - ")[0]) #separates the tuple at "-"" and returns the zeroth (first) position to variable

        #get the periodicity (daily or weekly) of the selected habit based on its ID
        periodicity = next(h[2] for h in habits if h[0] == habit_id)

        #get the current date and time
        today= datetime.now()

        #check if the habit is daily
        if periodicity == "daily":

            #format current time for comparison
            start_time = today.strftime("%Y-%m-%d %H:%M:%S")

            #query to check if the habit has already been marked as completed today
            cur.execute("""
                SELECT * FROM checkoffs 
                WHERE habit_id = ? AND DATE(checkoff_time) = DATE(?)""", 
                (habit_id, start_time))
            
        #check if the habit is weekly
        elif periodicity == "weekly":

            #get the start of the current week (Monday)
            week_start = today - timedelta(days=today.weekday())

            #query to check if the habit has already been marked as completed this week
            cur.execute("""
                SELECT * FROM checkoffs 
                WHERE habit_id = ? AND DATE(checkoff_time) >= DATE(?)""", 
                (habit_id, week_start.strftime("%Y-%m-%d")))

        #fetch the result of the check (if already completed)
        already_completed = cur.fetchone()

        #if a result exists, inform the user the habit is already completed in the period
        if already_completed:
            click.echo("You have already checked off this habit in this period.")
        else:
            #if not yet completed, insert a new record into the checkoffs table with the current time
            cur.execute("""
            INSERT INTO checkoffs (habit_id, checkoff_time)
            VALUES (?, ?)""", 
            (habit_id, today.strftime("%Y-%m-%d %H:%M:%S")))

        click.echo("Habit successfully checked off!")

        con.commit()
        con.close()



    #method for creating default habits
    def create_default_habits(user_id, db_path, username):

        #creates a path to the predefined habits.json file in the data subfolder
        #the result depends on the operating system
        json_path = os.path.join("data", "predefined_habits.json")

        #load JSON-file to read; encodeing="utf-8" most widely used character set worldwide
        with open(json_path, "r", encoding="utf-8") as file:
            habits = json.load(file)

        #select five random habits
        random_habits = random.sample(habits, 5)

        #current date for storage
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #connection to database
        con = sqlite3.connect(db_path)
        con.execute("PRAGMA foreign_keys = ON") #SQLite supports foreign keys, or relationships between tables, but they're disabled by default 
                                                #for them to work, you have to explicitly enable them—that's exactly what this command does -> Without (PRAGMA foreign_keys = ON) You can accidentally delete a user without automatically deleting the associated habits
        cur = con.cursor()

        #saves random habits in database
        for habit in random_habits:
            cur.execute("""
                INSERT INTO habits (user_id, habit_name, description, periodicity, creation_datetime) VALUES (?, ?, ?, ?, ?)""", 
                (user_id, habit["habit_name"], habit["description"], habit["periodicity"], now
            ))

        #ends connection to database and writes something on command line
        con.commit()
        con.close()
        print(f"Five random habits saved for user {username} (ID: {user_id}).")

                         
                         