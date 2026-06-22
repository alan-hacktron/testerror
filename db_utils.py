import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL injection vulnerability - user input concatenated directly into query
    query = "SELECT * FROM users WHERE username = '" + username + '"
    cursor.execute(query)
    return cursor.fetchone()

def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Another SQL injection - no parameterized query
    sql = "SELECT id FROM users WHERE username = '" + username + ' AND password = '" + password + '"
    cursor.execute(sql)
    return cursor.fetchone() is not None

