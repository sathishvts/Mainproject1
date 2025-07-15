






from datetime import datetime

# Sample invoice data
invoice_data = {
    "invoice_number": "INV-001",
    "client_name": "John Doe",
    "date": datetime.now().strftime("%d-%m-%Y"),
    "items": [
        {"description": "Web Design", "quantity": 1, "unit_price": 5000},
        {"description": "Hosting", "quantity": 12, "unit_price": 200},
        {"description": "Maintenance", "quantity": 6, "unit_price": 500},
    ]
}

# Generate HTML rows for items
items_html = ""
total_amount = 0
for item in invoice_data["items"]:
    line_total = item["quantity"] * item["unit_price"]
    total_amount += line_total
    items_html += f"<tr><td>{item['description']}</td><td>{item['quantity']}</td><td>{item['unit_price']}</td><td>{line_total}</td></tr>\n"

# Read template
with open("invoice_template.html", "r") as file:
    template = file.read()

# Fill in the template
filled_html = template.format(
    invoice_number=invoice_data["invoice_number"],
    date=invoice_data["date"],
    client_name=invoice_data["client_name"],
    items_html=items_html,
    total=total_amount
)

# Save to .html
output_filename = f"Invoice_{invoice_data['invoice_number']}.html"
with open(output_filename, "w") as file:
    file.write(filled_html)

print(f"Invoice saved to {output_filename}")
