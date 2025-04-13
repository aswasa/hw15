import sqlite3

connection=sqlite3.connect('mybot.db', check_same_thread=False)

sql=connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(tg_id INTEGER, name TEXT, number TEXT, location1 TEXT, location2 TEXT);')
connection.commit()

sql.execute('CREATE TABLE IF NOT EXISTS tables'
            '(table_id INTEGER PRIMARY KEY AUTOINCREMENT, chairs INTEGER, type TEXT, status TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS guests'
            '(tg_id INTEGER, table_id INTEGER);')

def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;',(tg_id,)).fetchone():
        return True
    else:
        return False

def check_name(tg_id):
    name = sql.execute('SELECT name FROM users WHERE tg_id=?;', (tg_id,)).fetchone()[0]
    return name

def register(tg_id, user_name, user_num, user_loc1, user_loc2):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?);', (tg_id, user_name, user_num, user_loc1, user_loc2))
    connection.commit()

def add_table(chairs, type, status = 'non-reserved'):
    sql.execute('INSERT INTO tables (chairs, type, status) VALUES (?, ?, ?);', (chairs, type, status))
    connection.commit()

def delete_table(table_id):
    sql.execute('DELETE FROM tables WHERE table_id=?;', (table_id,))
    connection.commit()

def reserve_table(tg_id, table_id):
    sql.execute('INSERT INTO guests VALUES (?, ?);', (tg_id, table_id))
    sql.execute('UPDATE tables SET status="reserved" WHERE table_id=?;', (table_id,))
    connection.commit()

def cancel_reservation(tg_id, table_id):
    sql.execute('DELETE FROM guests WHERE tg_id=? AND table_id=?;', (tg_id, table_id))
    sql.execute('UPDATE tables SET status="non-reserved" WHERE table_id=?;', (table_id,))
    connection.commit()

def find_table(chairs, type, status="non-reserved"):
    if sql.execute('SELECT table_id FROM tables WHERE chairs=? AND type=? AND status=?;', (chairs, type, status)).fetchone():
        return True
    else:
        return False

def show_id(chairs, type, status="non-reserved"):
    table_id = sql.execute('SELECT table_id FROM tables WHERE chairs=? AND type=? AND status=?;', (chairs, type, status)).fetchone()[0]
    return table_id

def check_reservation(tg_id):
    if sql.execute('SELECT * FROM guests WHERE tg_id=?;',(tg_id,)).fetchone():
        return True
    else:
        return False

def check_table1(tg_id):
    table = sql.execute('SELECT table_id FROM guests WHERE tg_id=?;', (tg_id,)).fetchone()[0]
    return table

def check_table(table_id):
    jj = sql.execute('SELECT chairs, type FROM tables WHERE table_id=?;', (table_id,)).fetchone()
    return jj


