from werkzeug.datastructures import CallbackDict

# Callback to run when session is modified
def on_session_update(session):
    print("📝 Session modified:", dict(session))

# Initialize session-like storage
session = CallbackDict(on_update=on_session_update)

# Example usage
def login():
    username = input("Enter username: ").strip()
    session['username'] = username
    print(f"✅ {username} is now logged in.")

def logout():
    if 'username' in session:
        print(f"👋 {session['username']} has been logged out.")
        session.clear()
    else:
        print("⚠️ No user is currently logged in.")

def view_session():
    print("📦 Current session data:", dict(session))

# Menu loop
def menu():
    while True:
        print("\n=== CLI Session Emulator ===")
        print("1. Login")
        print("2. View Session")
        print("3. Logout")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            login()
        elif choice == "2":
            view_session()
        elif choice == "3":
            logout()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

menu()
