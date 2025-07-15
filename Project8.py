import requests

def fetch_github_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        print(" GitHub user not found.")
        return

    data = response.json()
    print(f"\n GitHub Profile: {data['login']}")
    print(f"Name: {data.get('name')}")
    print(f"Public Repos: {data['public_repos']}")
    print(f"Followers: {data['followers']}")
    print(f"Following: {data['following']}")
    print(f"Bio: {data.get('bio')}")
    print(f"Profile URL: {data['html_url']}")

# Example usage
username = input("Enter GitHub username: ")
fetch_github_profile(username)
