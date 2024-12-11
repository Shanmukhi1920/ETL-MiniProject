import pandas as pd
from datetime import datetime 



def transform(current_data, forecast_data):
    # Transform Current Weather
    current_df = pd.DataFrame()
    for data in current_data:
        temp_df = pd.DataFrame([{
            'city': data['name'],
            'timestamp': datetime.fromtimestamp(data['dt']),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'weather_desc': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'clouds': data['clouds']['all']
        }])
        current_df = pd.concat([current_df, temp_df])
    
    # Transform Forecast
    forecast_df = pd.DataFrame()
    for city_data in forecast_data:
        city = city_data['city']['name']
        for item in city_data['list']:
            temp_df = pd.DataFrame([{
                'city': city,
                'forecast_timestamp': item['dt_txt'],
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'pressure': item['main']['pressure'],
                'humidity': item['main']['humidity'],
                'weather_desc': item['weather'][0]['description'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind']['deg'],
                'clouds': item['clouds']['all'],
                'pop': item['pop']  # Probability of precipitation
            }])
            forecast_df = pd.concat([forecast_df, temp_df])
    
    return current_df, forecast_df


    