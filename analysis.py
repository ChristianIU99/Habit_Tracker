from datetime import datetime, timedelta #imports methods datetime and timedelta from library datetime
import questionary #library for menu selection
import sqlite3     #library for database
import click       #library for CLI



#function to show all current habits
def show_all_current_habits(user_id, db_path):

    #connect to the SQLite database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    #query all habits that belong to the given user
    cur.execute("""
        SELECT id, habit_name, description, periodicity, creation_datetime FROM habits WHERE user_id = ?""", 
        (user_id,))
    
    habits = cur.fetchall()
    con.close()

    #if no habits found, inform the user
    if not habits:
        click.echo("You haven't created any habits yet.")
        return

    #print out all the habits found
    click.echo("\nYour current habits:\n")
    for habit in habits:
        habit_id, name, description, periodicity, created = habit
        click.echo(f"{habit_id}: {name} ({periodicity}) , {description} (created at {created})")
    


#function to show all complete habits
def all_completed_habits(user_id, db_path):

    #connect to the database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    #query all checkoffs and join with habit names, sorted by time
    cur.execute("""
        SELECT habits.habit_name, checkoffs.checkoff_time FROM checkoffs JOIN habits ON checkoffs.habit_id = habits.id WHERE habits.user_id = ?
        ORDER BY checkoffs.checkoff_time DESC""", (user_id,))

    completions = cur.fetchall()
    con.close()

    #display results
    if not completions:
        click.echo("You haven't checked off any habits yet.")
    else:
        click.echo("All checked habits:")
        for name, date in completions:
            click.echo(f"  - {name} am {date}")



#method to show all habits with same periodicity
def all_habits_same_periodicity(user_id, db_path):

    #connection to database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    #choice of periodicity
    periodicity = questionary.select("Which periodicity?", choices=["daily", "weekly"]).ask()

    #select all habits with same periodicity from the registered user
    cur.execute("""
        SELECT habit_name FROM habits WHERE user_id = ? AND periodicity = ? """, (user_id, periodicity))

    habits = cur.fetchall()
    con.close()

    #check the habits
    if not habits:
        click.echo(f"No habits with periodicity '{periodicity}'.")
    else:
        click.echo(f"Habits with periodicity '{periodicity}':")
        for (name,) in habits:
            click.echo(f"  - {name}")



#method to show longest series to check off of all habits
def longest_series_all_habits(user_id, db_path):

    #connection to database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    #get all habits of the user
    cur.execute("""
        SELECT id, habit_name, periodicity FROM habits WHERE user_id = ?""", (user_id,))
    
    habits = cur.fetchall()

    longest_streak = 0
    top_habit = None

    #iterate through all habits to find the one with the longest streak
    for habit_id, name, periodicity in habits:
        streak = calculate_longest_streak(cur, habit_id, periodicity)
        if streak > longest_streak:
            longest_streak = streak
            top_habit = name
     
    con.close()

    #output result
    if top_habit:
        click.echo(f"Longest streak: {longest_streak} ({top_habit})")
    else:
        click.echo("No streaks found.")



#method to show longest series of a given habit
def longest_series_given_habit(user_id, db_path):

    #connection to database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    #get all habits
    cur.execute("SELECT id, habit_name, periodicity FROM habits WHERE user_id = ?", (user_id,))
    habits = cur.fetchall()

    #checks the tuple 
    if not habits:
        click.echo("No habits available.")
        return

    #create display choices: name (periodicity)
    habit_map = {f"{h[1]} ({h[2]})": h for h in habits}

    #let user choose a specific habit
    choice = questionary.select("Choose a habit:", choices=habit_map.keys()).ask()
    habit_id, name, periodicity = habit_map[choice]

    #calculate streak
    streak = calculate_longest_streak(cur, habit_id, periodicity)
    click.echo(f"Longest streak for '{name}': {streak}")
    con.close()



#helper function to calculate the longest streak
def calculate_longest_streak(cur, habit_id, periodicity):

    #get all checkoffs for this habit, sorted by time
    cur.execute("""
        SELECT checkoff_time FROM checkoffs WHERE habit_id = ? ORDER BY checkoff_time ASC""", (habit_id,))
    

    rows = cur.fetchall()
    if not rows:
        return 0

    #convert strings to datetime objects
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in rows]
    
    #initialize streak counters
    longest = current = 1

    #loop through each consecutive checkoff date
    for i in range(1, len(dates)):
        delta = dates[i].date() - dates[i - 1].date()

        #determine expected interval
        if periodicity == "daily":
            step = timedelta(days=1)
        elif periodicity == "weekly":
            step = timedelta(days=7)
        else:
            continue
        
         #check if current checkoff continues the streak
        if delta == step:
            current += 1
        elif delta > step:
            current = 1  #streak is broken

        #update longest streak if necessary
        longest = max(longest, current)

    #return result
    return longest


