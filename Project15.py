from jinja2 import Environment, FileSystemLoader
import os

# 1. Load user data (can be from DB, CSV, etc.)
user_data = {
    "name": "Sathish Kumar",
    "email": "sathish@example.com",
    "product": "Wireless Headphones",
    "address": "42, Tech Street, Chennai"
}

# 2. Setup Jinja2 environment
template_dir = os.path.dirname(__file__)  # Current folder
env = Environment(loader=FileSystemLoader(template_dir))

# 3. Load the template
template = env.get_template("email_template.html")

# 4. Render the template with user data
email_body = template.render(user_data)

# 5. Save the rendered email to a file
output_filename = f"email_{user_data['name'].replace(' ', '_')}.html"
with open(output_filename, "w", encoding="utf-8") as file:
    file.write(email_body)

print(f"Email rendered and saved to: {output_filename}")
