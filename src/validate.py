import pandas as pd
from datetime import datetime, timedelta

def validate(current_df, forecast_df):
    
    validation_errors = []
    
    # Check for missing values
    for df_name, df in [("Current Weather", current_df), ("Forecast", forecast_df)]:
        null_counts = df.isnull().sum()
        if null_counts.any():
            cols_with_nulls = null_counts[null_counts > 0].index.tolist()
            validation_errors.append(f"{df_name} contains null values in columns: {cols_with_nulls}")
    
    # Validate value ranges
    valid_ranges = {
        'temperature': (-50, 50),    # Celsius
        'feels_like': (-50, 50),     # Celsius
        'temp_min': (-50, 50),       # Celsius
        'temp_max': (-50, 50),       # Celsius
        'pressure': (900, 1100),     # hPa
        'humidity': (0, 100),        # Percentage
        'wind_speed': (0, 100),      # m/s
        'wind_deg': (0, 360),        # Degrees
        'clouds': (0, 100)           # Percentage
    }
    
    for df_name, df in [("Current Weather", current_df), ("Forecast", forecast_df)]:
        for col, (min_val, max_val) in valid_ranges.items():
            if col in df.columns:
                out_of_range = df[
                    (df[col] < min_val) | (df[col] > max_val)
                ]
                if not out_of_range.empty:
                    validation_errors.append(
                        f"{df_name}: {len(out_of_range)} values in '{col}' are outside valid range "
                        f"[{min_val}, {max_val}]"
                    )
    
    
    # Validate timestamps
    now = datetime.now()
    
    # Current weather shouldn't be more than 2 hours old
    old_current = current_df[
        current_df['timestamp'] < now - timedelta(hours=2)
    ]
    if not old_current.empty:
        validation_errors.append("Current weather data contains outdated timestamps")
    
    # Forecast should be future dates within 5 days
    invalid_forecast = forecast_df[
        (forecast_df['forecast_timestamp'] < now) | 
        (forecast_df['forecast_timestamp'] > now + timedelta(days=5))
    ]
    if not invalid_forecast.empty:
        validation_errors.append("Forecast contains invalid timestamps (past dates or >5 days)")
    
    # Temperature consistency check
    for df_name, df in [("Current Weather", current_df), ("Forecast", forecast_df)]:
        invalid_temp = df[df['temp_max'] < df['temp_min']]
        if not invalid_temp.empty:
            validation_errors.append(
                f"{df_name} contains inconsistent temperatures (max < min) for "
                f"{len(invalid_temp)} records"
            )
    
    
    # Raise error if any validations failed
    if validation_errors:
        error_msg = "\n".join(validation_errors)
        raise ValueError({error_msg})
    
    return True