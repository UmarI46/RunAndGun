import sqlite3, os
import hashlib
DB_NAME = "login.db"

def add_name(playerId, equipped,):#insets into table a new record
    cursor.execute('''INSERT INTO shop
    VALUES (?,?,?,?,?,?,?)''', (playerId,equipped,False,False,False,False,"0"))

def add_name2():#Makes a record with all values = NULL
    cursor.execute('''INSERT INTO gamelogs DEFAULT VALUES''')


def add_col(colName):#creates column in table
    cursor.execute(
        f"""
        ALTER TABLE shop
        ADD COLUMN {colName}
        """
        )
    
def delete(id):#Deletes from table
    cursor.execute(f'''DELETE from gameLogs where gamelog2 = {id}''')

    
def create_table():#creates new table in database
    cursor.execute('''CREATE TABLE shop
        (Player Id,
        equipped,
        Cos1,
        Cos2,
        Cos3,
        Cos4)
        ''')

def update(val):#updates pre existing record
    cursor.execute(f'''UPDATE login SET Password = {val} WHERE Player = {"1"}''')
    
if not os.path.isfile(DB_NAME):# creates data base if not existing
    database=sqlite3.connect(DB_NAME)
    cursor=database.cursor()
    create_table()
    
else:#opens database if existing
    database=sqlite3.connect(DB_NAME)
    cursor=database.cursor()

database=sqlite3.connect(DB_NAME)
cursor=database.cursor()
#create_table()
#add_name("2","1")
#add_col("Currency")
#delete(12)
#add_name2()
#update("Password1!")


database.commit()
database.close()
