import sqlite3

conn = sqlite3.connect('bdd.db')
cur = conn.cursor()
req = "CREATE TABLE reservation (id	integer, email TEXT, date NUMERIC, temps DATE, PRIMARY KEY(id AUTOINCREMENT));"
cur.execute(req)
conn.commit()
conn.close()