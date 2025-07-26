# Habit_Tracker
Your Habit Tracker App for a better life!

This app is a command-line-based habit tracking tool that allows users to conveniently create, manage and analyse their habits. The data is stored in a database.

Features
1.	User registration and login with password hashing (SHA-256)
2.	Creation, deletion and ticking off of daily and weekly habits
3.	Analysis functions:
4.	Listing of all ticked habits
5.	Display of habits with the same periodicity
6.	Longest streak for a habit or across all habits
7.	SQLite database for persistent data storage
8.	Predefined test database for use in unit tests
9.	Unit tests with ‘pytest’

Structure
1.	main.py → contains the main programme and guides you through the menu display 
2.	habit.py → contains the ‘Habit’ class with methods for habit management
3.	user.py → contains the ‘User’ class with methods for user management
4.	reglog.py → contains the function for registration, login and password hash
5.	db.py → initialisation of the database 
6.	analysis.py → functional programming, functions for analysing habit series 
7.	data (folder) → contains data for testing purposes 
8.	test (folder) → test modules implemented with the external tool “pytest” 
1.	test_habit.py
2.	test_analysis.py
3.	test_reglog.py






Installation and application
To use the application, all files must be downloaded and saved in a folder on your computer's desktop. In addition, you will need to install some additional libraries that are not included in Python by default. These include:
1.	questionary
2.	click
3.	pytest
To simplify the installation of the libraries, I have created a ‘requirements.txt’ file. This must also be downloaded and can then be installed in the computer's terminal as follows:
1.	pip install -r requirements.txt
This completes the basics for running the programme. The programme can then be run as follows:
1.	Open the terminal (command prompt) on your computer
2.	Change to the file directory (your folder) with  cd <your folder path>
3.	Example: cd C:\Users\<YourUser>\Desktop\<YourFolderName>
You can then simply run the programme directly in the terminal with:
1.	python main.py

Tools and libraries
1.	click – for user-friendly CLI interface
2.	questionary – for interactive input
3.	sqlite3 – integrated SQL database
4.	hashlib – secure password hashing
5.	pytest – unit testing
6.	random – for random habits
7.	os – for applications with system structures

Security
1.	Passwords are never stored in plain text
2.	SHA-256 hashing is used
3.	SQLite uses PRAGMA foreign_keys = ON to maintain data integrity



Test data
The test database (test_data.db) contains:
1.	1 sample user: testuser / password: dummyhash
2.	5 predefined habits
3.	4 weeks of checkoff data for realistic tests

Tests
The following command automatically runs the stored unit tests:
1.	Stay in the main directory of your programme or switch to the directory with 2.
2.	cd C:\Users\<YourUser>\Desktop\<YourFolderName>
3.	pytest
To do this, you must ensure that the file ‘data/test_data.db’ exists. 
For specific tests, you can also execute the following, for example:
1.	pytest tests/test_habit.py

Author
Name: Christian Oltmann
GitHub: ChristianIU99

