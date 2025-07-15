import requests

def convert_currency(from_currency, to_currency, amount):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)

    if response.status_code != 200:
        print(" Error fetching exchange rates.")
        return

    data = response.json()
    result = data['result']
    print(f"\n {amount} {from_currency.upper()} = {round(result, 2)} {to_currency.upper()}")

# Example usage
from_curr = input("From currency (e.g., USD): ")
to_curr = input("To currency (e.g., INR): ")
amt = float(input("Amount: "))
convert_currency(from_curr, to_curr, amt)
