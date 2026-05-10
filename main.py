import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("API_KEY")

# User input
city = input("Enter city name: ")

# WeatherAPI URL
url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

try:
    # Send request
    response = requests.get(url)

    # Convert response to JSON
    data = response.json()

    # Error handling
    if "error" in data:
        print("❌ Error:", data["error"]["message"])
        exit()

    # Extract weather details
    temperature = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    weather = data["current"]["condition"]["text"]
    wind_speed = data["current"]["wind_kph"]

    # Display weather
    print("\n===== CURRENT WEATHER =====")
    print(f"📍 City: {city}")
    print(f"🌡 Temperature: {temperature}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"☁ Condition: {weather}")
    print(f"🌬 Wind Speed: {wind_speed} kph")

    # Alert system
    alerts = []

    if temperature > 35:
        alerts.append("🔥 High Temperature Alert!")

    if humidity > 80:
        alerts.append("💧 High Humidity Alert!")

    if "rain" in weather.lower():
        alerts.append("🌧 Rain Alert!")

    if "storm" in weather.lower():
        alerts.append("⛈ Storm Alert!")

    # Display alerts
    print("\n===== ALERTS =====")

    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("✅ No weather alerts.")

    # Create report data
    report = {
        "Date": [datetime.now()],
        "City": [city],
        "Temperature": [temperature],
        "Humidity": [humidity],
        "Condition": [weather],
        "Wind Speed": [wind_speed]
    }

    # Convert to DataFrame
    df = pd.DataFrame(report)

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    # Save CSV report
    filename = f"reports/{city}_weather_report.csv"
    df.to_csv(filename, index=False)

    print(f"\n📁 Report saved as: {filename}")

    # =========================
    # VISUALIZATION
    # =========================

    plt.figure(figsize=(7, 5))

    labels = ["Temperature", "Humidity", "Wind Speed"]
    values = [temperature, humidity, wind_speed]

    plt.bar(labels, values)

    plt.title(f"Weather Report for {city}")
    plt.ylabel("Values")

    # Create outputs folder
    os.makedirs("outputs", exist_ok=True)

    # Save graph
    graph_filename = f"outputs/{city}_weather_chart.png"

    plt.savefig(graph_filename)

    print(f"📊 Graph saved as: {graph_filename}")

    # Show graph
    plt.show()

except Exception as e:
    print("❌ Error occurred:", e)