import sqlite3

# --- DB Setup ---
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")
conn.commit()

# --- CRUD Functions ---
def create_note(title, content):
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    print("Note added successfully.\n")

def read_notes():
    cursor.execute("SELECT id, title FROM notes")
    notes = cursor.fetchall()
    if notes:
        for note in notes:
            print(f"[{note[0]}] {note[1]}")
    else:
        print("No notes found.")

def view_note(note_id):
    cursor.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    if note:
        print(f"\nTitle: {note[0]}\nContent: {note[1]}\n")
    else:
        print("Note not found.")

def update_note(note_id, new_title, new_content):
    cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (new_title, new_content, note_id))
    conn.commit()
    print("Note updated successfully.\n")

def delete_note(note_id):
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    print("Note deleted successfully.\n")

# --- Menu Loop ---
def menu():
    while True:
        print("\n=== Simple Notes App ===")
        print("1. Create Note")
        print("2. View All Notes")
        print("3. View Note by ID")
        print("4. Update Note")
        print("5. Delete Note")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Enter title: ")
            content = input("Enter content: ")
            create_note(title, content)

        elif choice == "2":
            read_notes()

        elif choice == "3":
            note_id = int(input("Enter note ID: "))
            view_note(note_id)

        elif choice == "4":
            note_id = int(input("Enter note ID to update: "))
            new_title = input("New title: ")
            new_content = input("New content: ")
            update_note(note_id, new_title, new_content)

        elif choice == "5":
            note_id = int(input("Enter note ID to delete: "))
            delete_note(note_id)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

menu()
conn.close()
