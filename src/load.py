import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def load(current_df, forecast_df):
    try:
        # Database connection parameters
        conn = psycopg2.connect(
            database="weather_db",
            user="airflow",
            password="airflow",
            host="localhost",
            port="5432"
        )
        
        # Create a cursor
        cur = conn.cursor()

        # Delete old current weather data
        cur.execute("DELETE FROM current_weather")
        
        # Delete forecast data older than current timestamp
        cur.execute("DELETE FROM forecast_weather")
        
        # Insert current weather data
        for _, row in current_df.iterrows():
            cur.execute("""
                INSERT INTO current_weather 
                (city, timestamp, temperature, feels_like, temp_min, temp_max, 
                pressure, humidity, weather_desc, wind_speed, wind_deg, clouds)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['city'], row['timestamp'], row['temperature'], 
                row['feels_like'], row['temp_min'], row['temp_max'],
                row['pressure'], row['humidity'], row['weather_desc'],
                row['wind_speed'], row['wind_deg'], row['clouds']
            ))
        
        # Insert forecast weather data
        for _, row in forecast_df.iterrows():
            cur.execute("""
                INSERT INTO forecast_weather 
                (city, forecast_timestamp, temperature, feels_like, temp_min, 
                temp_max, pressure, humidity, weather_desc, wind_speed, 
                wind_deg, clouds, pop)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['city'], row['forecast_timestamp'], row['temperature'],
                row['feels_like'], row['temp_min'], row['temp_max'],
                row['pressure'], row['humidity'], row['weather_desc'],
                row['wind_speed'], row['wind_deg'], row['clouds'], row['pop']
            ))
        
        # Commit the transactions
        conn.commit()
        
        print(f"Successfully loaded {len(current_df)} current weather records")
        print(f"Successfully loaded {len(forecast_df)} forecast records")
        
    except Exception as e:
        print(f"Error loading data to PostgreSQL: {e}")
        conn.rollback()  # Rollback in case of error
        raise
        
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()