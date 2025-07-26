# Habit_Tracker
Your Habit Tracker App for a better life!

This app is a command-line-based habit tracking tool that allows users to conveniently create, manage and analyse their habits. The data is stored in a database.

1	Features
  •	User registration and login with password hashing (SHA-256)
  •	Creation, deletion and ticking off of daily and weekly habits
  •	Analysis functions:
  •	Listing of all ticked habits
  •	Display of habits with the same periodicity
  •	Longest streak for a habit or across all habits
  •	SQLite database for persistent data storage
  •	Predefined test database for use in unit tests
  •	Unit tests with ‘pytest’

2	Structure
  •	main.py → contains the main programme and guides you through the menu display 
  •	habit.py → contains the ‘Habit’ class with methods for habit management
  •	user.py → contains the ‘User’ class with methods for user management
  •	reglog.py → contains the function for registration, login and password hash
  •	db.py → initialisation of the database 
  •	analysis.py → functional programming, functions for analysing habit series 
  •	data (folder) → contains data for testing purposes 
  •	test (folder) → test modules implemented with the external tool “pytest” 
      o	test_habit.py
      o	test_analysis.py
      o	test_reglog.py

3	Installation and application
To use the application, all files must be downloaded and saved in a folder on your computer's desktop. In addition, you will need to install some additional libraries that are not included in Python by default. These include:
  •	questionary
  •	click
  •	pytest
To simplify the installation of the libraries, I have created a ‘requirements.txt’ file. This must also be downloaded and can then be installed in the computer's terminal as follows:

  •	pip install -r requirements.txt
  
This completes the basics for running the programme. The programme can then be run as follows:
  1.	Open the terminal (command prompt) on your computer
  2.	Change to the file directory (your folder) with  cd <your folder path>
  3.	Example: cd C:\Users\<YourUser>\Desktop\<YourFolderName>
You can then simply run the programme directly in the terminal with:
  •	python main.py

4	Tools and libraries
  •	click – for user-friendly CLI interface
  •	questionary – for interactive input
  •	sqlite3 – integrated SQL database
  •	hashlib – secure password hashing
  •	pytest – unit testing
  •	random – for random habits
  •	os – for applications with system structures

5	Security
  •	Passwords are never stored in plain text
  •	SHA-256 hashing is used
  •	SQLite uses PRAGMA foreign_keys = ON to maintain data integrity



6	Test data
The test database (test_data.db) contains:
  •	1 sample user: testuser / password: dummyhash
  •	5 predefined habits
  •	4 weeks of checkoff data for realistic tests

7	Tests
The following command automatically runs the stored unit tests:
  1.	Stay in the main directory of your programme or switch to the directory with 2.
  2.	cd C:\Users\<YourUser>\Desktop\<YourFolderName>
  3.	pytest
To do this, you must ensure that the file ‘data/test_data.db’ exists. 
For specific tests, you can also execute the following, for example:
  •	pytest tests/test_habit.py

8	Author
Name: Christian Oltmann
GitHub: ChristianIU99
