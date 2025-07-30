from habit import Habit  #imports class "Habit" from modul habit.py
from db import db_path   #imports parameter db_path from modul db.py
import questionary       #for menu selection
import click             #for Command Line Interface (CLI) 
import analysis          #own analysis modul with functions to analyse the habits   
import reglog            #own reglog modul with functions for register, login and password hash
import sys               #from standard library, which provides direct access to variables and functions related to the interpreter and the execution of the program
import db                #own db modul for initialisation



#turns the main() function into a standalone CLI command        
click.command()

#main function in which the database is initialized and the functions for the login/registration menu and the main menu are executed
def main():

    #the library click with the method echo, which show text on console (similar to print)
    #the text "Register/Login" is displayed
    click.echo("Registration/Login")

    #the function out of db.py is called an initializes the database
    db.init_db()
    
    #the function menu() is called and the tuple of the function are passed to user_data
    user_data = menu()
    
    #It checks whether user_data contains any values. If not, the menu function is aborted immediately.
    if user_data is None:
        return
    
    #unpacks the tuple from user_data into two variables
    user_id, username = user_data

    #the function main is called and gets the two values to use these
    mainmenu(user_id)



#in function menu() there is the choice between login, register and exit
def menu():

    #loop to repeat the login in case of failure
    while True:

        #shows the selection on the command line
        action = questionary.select(
                "What do you want to do?", #the text is shown on command line
                choices=["Login", "Register", "Exit"] #Options
            ).ask() #to ask iteractive input questions in the terminal

        #first option is register
        if action == "Register": 

            #called the function register of the modul reglog.py and passes the tuple with the user data and variable user_data and then passes it to caller
            user_data = reglog.register("unused", "unused")
            return user_data

        #second option is login
        elif action == "Login":
            
            #the function login of modul reglog.py is called and passes the tuple to login_register
            #checks variable if the tuple exists, if not function is repeated, if so, then the tuple is returned to caller
            login_result = reglog.login("unused", "unused")
            if login_result is None:
                continue
            else:
                return login_result

        #third option is exit    
        elif action == "Exit":
            click.echo("See you soon!") #show text on command line
            sys.exit() #terminates the program with immediate effect
    


#In the main menu you can choose what you want to do and the user_id is handed over
def mainmenu(user_id):
     
     #loop, if a failure goes wrong
     while True:

        #you can select between the possibilities
        action = questionary.select(
                "Welcome to your Habit Tracker! What do you want to do?",
                choices=["Create Habit", "Delete Habit", "Complete Habit", "Analysis Habits", "Exit"]
            ).ask()

        #option to create new habits    
        if action == "Create Habit":
            click.echo("Here you can create new habits!") #text on command line
            Habit.create_habit(user_id, db_path)          #method create_habit from class Habit with two parameters passed
            questionary.text("\nBack? Enter!").ask()      #text is a method of library questionary with the question Back? and press enter to return to the analysis selection
                                                          #\n = Line break
        #option to delete habits                                                  
        if action == "Delete Habit":
            click.echo("Here you can delete habits!")     #text on command line
            Habit.delete_habit(user_id, db_path)          #method delete_habit from class Habit with two parameters passed
            questionary.text("\nBack? Enter!").ask()      #text is a method of library questionary with the question Back? and press enter to return to the analysis selection

        #option to complete your habits
        if action == "Complete Habit":                           
            click.echo("Here you can check off your habits")     #text on command line   
            Habit.complete_habit(user_id, db_path)               #method delete_habit from class Habit with two parameters passed
            questionary.text("n\Back? Enter").ask()              #text is a method of library questionary with the question Back? and press enter to return to the analysis selection
        
        #option to analyse your habits
        if action == "Analysis Habits": 
            click.echo("Here you can analyse your habits!")      #text on command line 

            #Submenu for selecting the analysis function 
            while True:

                #selection of analysis function
                streak = questionary.select(
                        "Which streak of your habits would you like to see?",
                        choices = ["All current habits", "All completed Habits", "Habits with same periodicity", "Longest Streak of all habits", "Longest streak of a given habit", "Main menu"]
                    ).ask()

                #option to see all your current
                if streak == "All current habits":
                    click.echo("Here you can view your created habits!")    #text on command line
                    analysis.show_all_current_habits(user_id, db_path)      #function show_all_current_habits from modul analysis with assignment to the user via user_id
                    questionary.text("\nBack? Enter!").ask()                #text is a method of library questionary with the question Back? and press enter to return to the analysis selection

                #option to see all checked habits
                elif streak == "All completed Habits":
                   click.echo("Here you can see your checked habits!")      #text on command line
                   analysis.all_completed_habits(user_id, db_path)          #function all_completed_habits from modul analysis with assignment to the user via user_id
                   questionary.text("\nBack? Enter!").ask()                 #text is a method of library questionary with the question Back? and press enter to return to the analysis selection
                
                #option to see habits with same periodicity
                elif streak == "Habits with same periodicity":
                   click.echo("Here you can see habits with the same periodicity!")     #text on command line
                   analysis.all_habits_same_periodicity(user_id, db_path)               #function all_habits_same_periodicity from modul analysis with assignment to the user via user_id
                   questionary.text("\nBack? Enter!").ask()                             #text is a method of library questionary with the question Back? and press enter to return to the analysis selection
                
                #option to see longest streak of all habits
                elif streak == "Longest Streak of all habits":
                   click.echo("Here you can see your longest streak of all habits!")    #text on command line
                   analysis.longest_series_all_habits(user_id, db_path)                 #function longest_series_all_habits from modul analysis with assignment to the user via user_id
                   questionary.text("\nBack? Enter!").ask()                             #text is a method of library questionary with the question Back? and press enter to return to the analysis selection

                #option to see longest streak of a given habit
                elif streak == "Longest streak of a given habit":
                   click.echo("Here you can see your longest streak of a specific habit!")#text on command line
                   analysis.longest_series_given_habit(user_id, db_path)                  #function longest_series_given_habit from modul analysis with assignment to the user via user_id
                   questionary.text("\nBack? Enter!").ask()                               #text is a method of library questionary with the question Back? and press enter to return to the analysis selection

                #option to return to the main menu; ends the loop
                elif streak == "Main menu":
                    break
                
        #option to exit program directly                 
        if action == "Exit":
            click.echo("Thank you for your visit. See you later!")        
            sys.exit() #Method of library sys which ends the programm directly



#Executes the following block only when this script is started directly – not when it is imported
if __name__ == "__main__":
    main()
