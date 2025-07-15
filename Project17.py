import sqlite3
import hashlib

# --- DB Setup ---
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")
conn.commit()

# --- Password Hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Registration ---
def register():
    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()

    hashed = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("✅ Registered successfully!\n")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.\n")

# --- Login ---
def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    hashed = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, hashed))
    result = cursor.fetchone()

    if result:
        print(f"✅ Welcome, {username}!\n")
    else:
        print("❌ Login failed. Invalid username or password.\n")

# --- Main Menu ---
def menu():
    while True:
        print("=== User Login System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

menu()
conn.close()
