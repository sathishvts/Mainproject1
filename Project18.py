import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject1 REAL NOT NULL,
    subject2 REAL NOT NULL,
    subject3 REAL NOT NULL,
    average REAL NOT NULL
)
""")
conn.commit()

# --- Input Validator ---
def get_valid_mark(prompt):
    while True:
        try:
            mark = float(input(prompt))
            if 0 <= mark <= 100:
                return mark
            else:
                print("⚠️ Enter a mark between 0 and 100.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")

# --- Add Student ---
def add_student():
    name = input("Enter student name: ").strip()
    print("Enter marks (0-100):")
    m1 = get_valid_mark("Subject 1: ")
    m2 = get_valid_mark("Subject 2: ")
    m3 = get_valid_mark("Subject 3: ")
    avg = round((m1 + m2 + m3) / 3, 2)

    cursor.execute(
        "INSERT INTO students (name, subject1, subject2, subject3, average) VALUES (?, ?, ?, ?, ?)",
        (name, m1, m2, m3, avg)
    )
    conn.commit()
    print(f"✅ Student '{name}' added with average: {avg}\n")

# --- View Students ---
def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if not rows:
        print("⚠️ No student records found.")
        return
    print("\n--- Student Records ---")
    print(f"{'ID':<3} {'Name':<15} {'Sub1':>5} {'Sub2':>5} {'Sub3':>5} {'Avg':>6}")
    print("-" * 45)
    for row in rows:
        print(f"{row[0]:<3} {row[1]:<15} {row[2]:>5} {row[3]:>5} {row[4]:>5} {row[5]:>6}")
    print()

# --- Menu Loop ---
def menu():
    while True:
        print("=== Student Mark Tracker ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

menu()
conn.close()
