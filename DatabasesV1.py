import sqlite3, os

#creates the database for username and passwords
database=sqlite3.connect("LogIn_Leaderboard.db")
cursor=database.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS
Users(UsernameL text,
Password text)
''')
cursor.execute('''SELECT * FROM Users''')
results=cursor.fetchall()

#creating the leaderboard database
database=sqlite3.connect("LogIn_Leaderboard.db")
cursor=database.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS
Scoreboard(UsernameS text,
Score intenger,
Rank intenger)
''')
DefaultScore=0
DefaultRank=999


#rerplaces all NULL values
cursor.execute('''UPDATE Scoreboard SET Score=0 WHERE Score IS NULL  ''')
database.commit()
cursor.execute('''UPDATE Scoreboard SET Rank=999 WHERE Rank IS NULL  ''')
database.commit()


database.close()
