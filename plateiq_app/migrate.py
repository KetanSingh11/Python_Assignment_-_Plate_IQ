import sqlite3
f = open("schema.sql")

conn = sqlite3.connect("data.db")
conn.executescript(f.read().strip())
conn.commit()

f.close()