import sys
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if variable is loaded
api_key = os.getenv('weather_api_key')

currentWeather_url = 'http://api.openweathermap.org/data/2.5/weather'
forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
cities = ['Chicago', 'New York','San Franciso','Austin']

def extract():
    current_weather = []
    forecast_weather = []
    for city in cities:
        # Parameter for API calls
        params = {
            'q': city ,
            'appid': api_key,
            'units': 'metric'
            }
        # for given city - Get current weather information
        current_response = requests.get(currentWeather_url,params)
        if current_response.status_code == 200:
            current_weather.append(current_response.json())

        # for given city - Get 5 days forecast information
        forecast_response = requests.get(forecast_url,params)
        if forecast_response.status_code == 200:
            forecast_weather.append(forecast_response.json())

    return current_weather,forecast_weather
