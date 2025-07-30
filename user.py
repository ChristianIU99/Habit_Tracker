from db import db_path
from os.path import join, abspath, dirname ##imports three functions of standard library os.path
import sqlite3 #imports sqlite database



#class "User"
class User:

    #here you can see the class "User", which creates a user and saves the data username and password in a sqlite3 database

    #the method "__init__" is a specially method, which automatically executes when an object of the class was created 
    def __init__(self, username, password):
        
        #self is a reference to the object itself
        #firstname and password are parameters passed when creating a new object
        self.username = username
        self.password = password
        self.user_id = None      #set later

        #connection to the sqlite database is established under the db_path
        #self.conn saves this connection object and allows later saving with "commit()"
        self.con = sqlite3.connect(db_path)

        #"cursor()" is an control object that allows to execute sql queries such as SELECT, INSERT, UPDATE, etc.
        #self.cur saves the cursor, so that you can access the database later
        self.cur = self.con.cursor()



    #method to store username and password in database
    def store_user_in_db(self):

        #executes a sql INSERT-statement 
        #insert an new record with two values into the users table
        #placeholder ?, ? are replaced by self.username and self.password
        self.cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", (self.username, self.password))
                        
        #saves the changes permanently in database
        self.con.commit()

        #saves the ID of added user
        self.user_id = self.cur.lastrowid   #method I get the ID of the user

        return self.user_id   #returns user_id

        

        
