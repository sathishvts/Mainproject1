# # <!DOCTYPE html>
# # <html>
# # <head><title>{{ site_title }}</title></head>
# # <body>
# #   <h1>{{ site_title }}</h1>
# #   <ul>
# #     {% for page in pages %}
# #       <li><a href="{{ page.url }}">{{ page.name }}</a></li>
# #     {% endfor %}
# #   </ul>
# # </body>
# # </html>

# # from jinja2 import Template


# data = {
#     "site_title": "My Static Site",
#     "pages": [
#         {"name": "Home", "url": "index.html"},
#         {"name": "About", "url": "about.html"},
#         {"name": "Contact", "url": "contact.html"}
#     ]
# }

# with open("template.html") as f:
#     template = Template(f.read())

# output = template.render(data)

# with open("output.html", "w") as f:
#     f.write(output)

# print("✅ Static site generated: output.html")
