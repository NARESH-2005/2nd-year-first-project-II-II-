import requests
import time

# Constants
API_KEY = "dab9f5705059854dc9dfbca382781b35"  # Your OpenWeatherMap API key

# Function to get the user's location based on IP address
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        city = data.get("city", "Unknown City")
        country = data.get("country", "Unknown Country")
        return {"city": city, "country": country}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None

# Function to fetch real-time weather data
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"] * 3.6  # Convert to km/h
        weather_desc = data["weather"][0]["description"]
        return {"temperature": temperature, "humidity": humidity, "wind_speed": wind_speed, "weather_desc": weather_desc}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None

# Function to provide travel advice based on temperature
def give_temperature_advice(temperature):
    if temperature > 40:
        return "🔥 It's extremely hot! It's not safe for traveling, consider postponing your trip."
    elif temperature < 0:
        return "❄️ It's freezing! Traveling is not recommended, stay safe and warm indoors."
    elif temperature > 30:
        return "🌞 It's very hot. Make sure to stay hydrated and wear sunscreen!"
    elif temperature < 10:
        return "🧣 It's cold. Consider wearing warm clothes and avoid unnecessary outdoor activities."
    else:
        return "🌤️ Weather is pleasant, safe for travel!"

# Function to send weather alerts (Storm, Rain, Snow, Extreme Cold)
def send_weather_alert(city, temperature, weather_desc):
    significant_conditions = ["storm", "rain", "snow"]
    alert_message = f"\n⚠️ Weather Alert for {city}: "
    alert_triggered = False
    for condition in significant_conditions:
        if condition in weather_desc.lower():
            alert_message += f"{condition.capitalize()} expected! Take precautions. "
            alert_triggered = True
    if temperature < 5:
        alert_message += "❄️ Extreme Cold Alert! Stay warm and avoid prolonged exposure outside."
        alert_triggered = True
    if alert_triggered:
        print(alert_message)
    else:
        print(alert_message+f"✅ No severe weather alerts for {city}.")

# Function to recommend clothing based on temperature
def get_clothing_recommendation(temperature):
    recommendations = {
        "child": {
            "hot": "🧢 Light cotton clothes, hat, and sunscreen. Keep kids hydrated!",
            "warm": "👕 T-shirt, shorts, and a cap.",
            "cool": "🧥 A light jacket with a full-sleeve shirt.",
            "cold": "🧣 Layered clothing, gloves, woolen hat, and insulated shoes.",
        },
        "elder": {
            "hot": "🌞 Loose cotton clothes, hat, sunglasses, and drink plenty of water!",
            "warm": "👚 Comfortable full-sleeve shirt and light trousers.",
            "cool": "🧥 A sweater or light jacket.",
            "cold": "🧣 Heavy wool clothing, thermal innerwear, and warm socks.",
        },
        "adult": {
            "hot": "😎 Light cotton T-shirt and shorts. Stay cool and drink water!",
            "warm": "👖 T-shirt and jeans work well. Carry sunglasses!",
            "cool": "🧥 A hoodie or light jacket.",
            "cold": "🧣 Heavy jacket, gloves, and thermal socks.",
        }
    }

    if temperature > 30:
        temp_category = "hot"
    elif 20 <= temperature <= 30:
        temp_category = "warm"
    elif 10 <= temperature < 20:
        temp_category = "cool"
    else:
        temp_category = "cold"

    return (
        f"👶 Children: {recommendations['child'][temp_category]}\n"
        f"👨 Adults: {recommendations['adult'][temp_category]}\n"
        f"👴 Elders: {recommendations['elder'][temp_category]}"
    )

# Function to display weather and alerts
def display_weather_info(city, api_key):
    weather_data = get_weather_data(city, api_key)
    if weather_data:
        print("\n🌍 Real-Time Weather Update:")
        print(f"📍 Location: {city}")
        print(f"🌡️ Temperature: {weather_data['temperature']}°C")
        print(f"💧 Humidity: {weather_data['humidity']}%")
        print(f"💨 Wind Speed: {weather_data['wind_speed']} km/h")
        print(f"🌤️ Conditions: {weather_data['weather_desc']}")
        
        # Get clothing recommendation
        clothing_advice = get_clothing_recommendation(weather_data["temperature"])
        print(f"\n👕 Clothing Recommendation:\n{clothing_advice}")

        # Get travel safety advice
        travel_advice = give_temperature_advice(weather_data["temperature"])
        print(f"\n🚗 Travel Advice:\n{travel_advice}")

        # Send weather alert
        send_weather_alert(city, weather_data["temperature"], weather_data["weather_desc"])
    else:
        print("Could not fetch current weather data.")

# Function to send periodic weather notifications
def send_continuous_notifications(city, api_key, interval):
    while True:
        display_weather_info(city, api_key)
        print(f"📢 Next update in {interval} seconds... (Type 'stop' to cancel)")
        time.sleep(interval)
        stop = input("Enter 'stop' to stop notifications: ").strip().lower()
        if stop == "stop":
            print("✅ Notifications stopped.")
            break

# Main function
if __name__ == "__main__":
    if not API_KEY:
        print("API key is missing! Set it as an environment variable.")
    else:
        user_location = get_user_location()
        if user_location:
            print(f"\nFetching weather updates for: {user_location['city']}, {user_location['country']}...")
            display_weather_info(user_location["city"], API_KEY)
        
        while True:
            custom_city = input("\nDo you want to check another location? (Enter city name or type 'no' to exit): ").strip().lower()
            if custom_city == "no":
                print("\n✅ Exiting. Stay safe! 🌞")
                break
            elif custom_city:
                display_weather_info(custom_city, API_KEY)
            
            notify = input("\nDo you want continuous weather updates? (yes/no): ").strip().lower()
            if notify == "yes":
                try:
                    interval = int(input("Enter update interval in seconds (e.g., 60 for 1 min): ").strip())
                    send_continuous_notifications(custom_city, API_KEY, interval)
                except ValueError:
                    print("⚠️ Invalid input. Please enter a number.")
