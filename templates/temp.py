import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, role TEXT)")
conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, image TEXT)")

# Create admin
conn.execute("INSERT INTO users (name, password, role) VALUES ('admin', 'admin', 'admin')")

conn.commit()
conn.close()