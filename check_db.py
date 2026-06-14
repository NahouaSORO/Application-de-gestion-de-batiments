import sqlite3

chemin = "D:\\Atlas_Bâtiment\\Atlas.db"
conn = sqlite3.connect(chemin)
cur = conn.cursor()

print("=== TABLE users ===")
cur.execute("SELECT * FROM users")
users = cur.fetchall()
for row in users:
    print(row)

conn.close()

