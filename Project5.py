import json
import os

SETTINGS_FILE = 'settings.json'

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"theme": "light", "language": "en"}
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
    print(f"✅ Updated: {key} = {value}")

# Example usage
settings = load_settings()
print("🔧 Current Settings:", settings)

update_setting("theme", "dark")
update_setting("language", "fr")
