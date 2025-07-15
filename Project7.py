import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print(" Failed to fetch weather data.")
        return

    data = response.json()
    print(f"\n Weather in {data['name']}, {data['sys']['country']}:")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Weather: {data['weather'][0]['description'].capitalize()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind: {data['wind']['speed']} m/s")

# Example usage
city = input("Enter city name: ")
get_weather(city, api_key="YOUR_API_KEY_HERE")
