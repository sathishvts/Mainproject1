from werkzeug.security import generate_password_hash, check_password_hash

def hash_password():
    password = input("Enter a password to hash: ").strip()
    hashed = generate_password_hash(password)
    print(f"\n🔐 Hashed password:\n{hashed}\n")
    return hashed

def verify_password(hashed):
    password = input("Enter password to verify: ").strip()
    if check_password_hash(hashed, password):
        print("✅ Password is correct!")
    else:
        print("❌ Incorrect password.")

def menu():
    hashed = None
    while True:
        print("\n=== Password Hashing Tool ===")
        print("1. Hash a password")
        print("2. Verify password")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            hashed = hash_password()
        elif choice == "2":
            if hashed:
                verify_password(hashed)
            else:
                print("⚠️ No password hashed yet. Choose option 1 first.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

menu()
