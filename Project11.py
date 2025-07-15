import re

def validate_password(pwd):
    if len(pwd) < 8:
        print(" Password too short (min 8 characters).")
    elif not re.search(r"[A-Z]", pwd):
        print(" Missing uppercase letter.")
    elif not re.search(r"[0-9]", pwd):
        print(" Missing digit.")
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        print(" Missing special character.")
    else:
        print(" Password is strong.")

# Example usage
password = input("Enter password to validate: ")
validate_password(password)
