import json
import os

def display_resume(path):
    if not os.path.exists(path):
        print(f" File not found: {path}")
        return

    with open(path, 'r') as f:
        resume = json.load(f)

    print(f"\n👤 Name: {resume['name']}")
    print(f" Email: {resume['email']}")
    print("\n Skills:")
    for skill in resume['skills']:
        print(f" - {skill}")

    edu = resume['education']
    print("\n Education:")
    print(f" - {edu['degree']} from {edu['university']} ({edu['year']})")

    print("\n Experience:")
    for exp in resume['experience']:
        print(f" - {exp['role']} at {exp['company']} ({exp['years']})")

# Example usage
display_resume("resume.json")
