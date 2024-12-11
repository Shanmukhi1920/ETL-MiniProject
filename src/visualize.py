import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def visualize(current_df, forecast_df, output_dir='./visualizations'):
    """
    Create various weather visualizations and save them to the output directory
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Forecast Temperature Trends
    plt.figure(figsize=(15, 8))
    for city in forecast_df['city'].unique():
        city_data = forecast_df[forecast_df['city'] == city]
        plt.plot(city_data['forecast_timestamp'], 
                city_data['temperature'], 
                label=city, 
                marker='o')
    plt.title('Temperature Forecast Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/forecast_trends.png')
    plt.close()
    
    # 2. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_cols = ['temperature', 'feels_like', 'humidity', 'wind_speed', 'clouds']
    correlation = current_df[numeric_cols].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('Weather Metrics Correlation')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_heatmap.png')
    plt.close()
    
    # 3. Precipitation Probability Forecast
    if 'pop' in forecast_df.columns:
        plt.figure(figsize=(15, 8))
        for city in forecast_df['city'].unique():
            city_data = forecast_df[forecast_df['city'] == city]
            plt.plot(city_data['forecast_timestamp'], 
                    city_data['pop'] * 100, 
                    label=city, 
                    marker='o')
        plt.title('Precipitation Probability Forecast')
        plt.xlabel('Date')
        plt.ylabel('Precipitation Probability (%)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/precipitation_forecast.png')
        plt.close()


