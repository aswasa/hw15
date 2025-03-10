import sqlite3

connection=sqlite3.connect('mybot.db', check_same_thread=False)

sql=connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(tg_id INTEGER, name TEXT, number TEXT, location1 TEXT, location2 TEXT);')

def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;',(tg_id,)).fetchone():
        return True
    else:
        return False

def check_name(tg_id):
    sql.execute('SELECT name FROM users WHERE tg_id=?;', (tg_id,)).fetchone()

def register(tg_id, user_name, user_num, user_loc1, user_loc2):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?);', (tg_id, user_name, user_num, user_loc1, user_loc2))
    connection.commit()