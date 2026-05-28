import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS words(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    english TEXT,
    turkish TEXT,
    sample TEXT,
    picture TEXT,
    correct_count INTEGER DEFAULT 0,
    learned INTEGER DEFAULT 0
)
""")

connection.commit()

connection.close()

print("Veritabanı oluşturuldu")
