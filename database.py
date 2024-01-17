# database.py
import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, email TEXT, birthdate TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_user(name, email, birthdate, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?,?)", (name, email, birthdate, password))
    conn.commit()
    conn.close()

def verify_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

