import re

def extract_emails(file_path):
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        print(f"\n Found {len(emails)} email(s):")
        for email in set(emails):
            print(f" - {email}")
    except FileNotFoundError:
        print(" File not found.")

# Example usage
extract_emails("sample.txt")
