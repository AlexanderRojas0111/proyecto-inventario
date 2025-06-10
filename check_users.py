import sqlite3

DATABASE = 'inventario.db'

def check_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    for user in users:
        print(user)
    conn.close()

if __name__ == "__main__":
    check_users()
