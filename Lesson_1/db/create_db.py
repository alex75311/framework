import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
with open('create_db.sql', 'r', encoding='utf-8') as f:
    sql = f.read()
cur.executescript(sql)
cur.close()
con.close()
