#!/usr/bin/env python3

import requests
import argparse
from termcolor import colored
from datetime import datetime

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Get 7-day weather forecast for a city.")
parser.add_argument("city", help="The city to get the weather for")
args = parser.parse_args()

# Get city coordinates (latitude and longitude) using Open-Meteo
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={args.city}&language=en&count=1"
geo_response = requests.get(geo_url)
if geo_response.status_code != 200:
    print(f"Error: Unable to retrieve city coordinates. Status Code: {geo_response.status_code}")
    exit()

geo_data = geo_response.json()
lat = geo_data["results"][0]["latitude"]
lon = geo_data["results"][0]["longitude"]

# Construct Open-Meteo API URL for 7-day forecast (including weather description)
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=Europe%2FIstanbul"

# Make API request and parse response
response = requests.get(url)
if response.status_code != 200:
    print(f"Error: Unable to retrieve weather forecast. Status Code: {response.status_code}")
    exit()

data = response.json()

# Parse daily weather data for the next 7 days
forecast = data["daily"]

# Weather code to description and emoji mapping
weather_codes = {
    0: ("Clear", "☀️"),
    1: ("Partly Cloudy", "🌤"),
    2: ("Cloudy", "☁️"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫"),
    48: ("Rime Fog", "🌫"),
    51: ("Light Rain", "🌧"),
    53: ("Moderate Rain", "🌧"),
    55: ("Heavy Rain", "🌧"),
    56: ("Light Freezing Rain", "🌨"),
    57: ("Heavy Freezing Rain", "🌨"),
    61: ("Light Showers", "🌦"),
    63: ("Moderate Showers", "🌦"),
    65: ("Heavy Showers", "🌦"),
    66: ("Light Freezing Showers", "🌨"),
    67: ("Heavy Freezing Showers", "🌨"),
    71: ("Light Snow", "❄️"),
    73: ("Moderate Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    77: ("Snow Grains", "❄️"),
    80: ("Light Showers of Rain", "🌧"),
    81: ("Moderate Showers of Rain", "🌧"),
    82: ("Heavy Showers of Rain", "🌧"),
    85: ("Light Snow Showers", "❄️"),
    86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with Light Hail", "⛈️"),
    99: ("Thunderstorm with Hail", "⛈️")
}

# Function to get the day of the week from the date
def get_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A")  # Returns the full name of the day (e.g., Monday)

# Print header with bold and colored text
print(colored(f"\n🌦 7-Day Weather Forecast for {args.city.capitalize()} 🌦", "cyan", attrs=["bold"]))

# Loop through each day's data
for i in range(len(forecast["temperature_2m_max"])):
    date = forecast["time"][i]  # Get the date for the day
    day_of_week = get_day_of_week(date)  # Get the day of the week
    temperature_max = forecast["temperature_2m_max"][i]  # Max temperature for the day
    temperature_min = forecast["temperature_2m_min"][i]  # Min temperature for the day
    precipitation = forecast["precipitation_sum"][i]  # Precipitation for the day
    weather_code = forecast["weathercode"][i]  # Get weather code for the day
    weather_description, weather_emoji = weather_codes.get(weather_code, ("Unknown", "❓"))  # Get description and emoji

    # Print each day's data with color-coded temperatures and weather information
    print(f"\n{colored(f'{date} ({day_of_week})', 'yellow', attrs=['bold'])}:")
    print(f"  {colored(f'Max Temp: {temperature_max:.1f}°C', 'green', attrs=['bold'])} | "
          f"{colored(f'Min Temp: {temperature_min:.1f}°C', 'blue', attrs=['bold'])} | "
          f"{colored(f'Precipitation: {precipitation:.1f} mm', 'magenta', attrs=['bold'])}")
    print(f"  {colored(f'Weather: {weather_description} {weather_emoji}', 'red', attrs=['bold'])}")
