from os.path import join, dirname, abspath, exists #imports four functions of standard library os.path
import sqlite3 #imports sqlite database



#creates the full path to the UserHabit.db file, relative to the location of the current Python file
#__file__ is a special variable which executes the current path of the Python file
#abspath(__file__) changes path into absolute path
#dirname(..) gets the folder where the file is located
#join adds the database to the folder path
db_path = join(dirname(abspath(__file__)), 'HabitUser.db')



#function to initialize the database "HabitUser.db"
def init_db():

    #checks if the database exists, if not it is created with the corresponding tables
    if not exists(db_path):
        con = sqlite3.connect(db_path) #connection to database
        cur = con.cursor() #creates a cursor object that is necessary to execute SQL commands with a database connection.

        #create table users if not exists with columns id, username, password
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT ,
                password TEXT 
            )
        """)

        #creates table habits if not exists with columns id, user_id, habit_name, periodicity, description, creation_datetime
        #you don't have to manually delete (no extra DELETE FROM habits WHERE user_id = ? required)
        #It prevents orphan records (i.e., entries in habits that no longer have a valid user)
        #It keeps your database clean and consistent
        #id of the habit is passed to userID to identify the habit with the user, if a user is deleted the associated habits are also deleted
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                habit_name TEXT NOT NULL,
                periodicity TEXT,
                description TEXT,
                creation_datetime datetime,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  
            )
        """) 

        #creates table checkoffs if not exists with columns user_id, habid, id, checkoff_time
        cur.execute("""
            CREATE TABLE IF NOT EXISTS checkoffs (
                user_id INTEGER, 
                habit_id INTEGER, 
                checkoff_time datetime
            )        
        """)

        con.commit() #saves changes permanently
        con.close()  #close connection to database; important to free up resources and avoid read/write locks
    else:
        pass #otherwise nothing happens