import pandas as pd
import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Get Airflow home directory and update Python path
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/root/airflow')
sys.path.append(AIRFLOW_HOME)

# Import modules from src
try:
    from src.extract import extract
    from src.transform import transform
    from src.load import load
    from src.visualize import visualize
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    raise

# Import functions into global scope for tasks
_extract = extract
_transform = transform
_load = load
_visualize = visualize

def ensure_temp_dir():
    """Ensure temp directory exists"""
    temp_dir = os.path.join(AIRFLOW_HOME, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'weather_etl',
    default_args=default_args,
    description='Weather ETL Pipeline with Visualization',
    schedule_interval='@daily',
    catchup=False
)

def run_extract_transform(**context):
    try:
        logger.info("Starting extract and transform process")

        # Get temp directory
        temp_dir = ensure_temp_dir()
        
        # Extract data
        current_data, forecast_data = _extract()
        logger.info("Data extraction completed")
        
        # Transform data
        current_df, forecast_df = _transform(current_data, forecast_data)
        logger.info("Data transformation completed")
        
        
        # Save to temporary CSV files
        current_path = os.path.join(temp_dir, 'current_weather.csv')
        forecast_path = os.path.join(temp_dir, 'forecast_weather.csv')
        
        current_df.to_csv(current_path, index=False)
        forecast_df.to_csv(forecast_path, index=False)
        
    except Exception as e:
        logger.error(f"Error in extract_transform task: {str(e)}")
        raise

def run_visualize(**context):
    try:
        logger.info("Starting visualization process")
        
        # Get temp directory
        temp_dir = ensure_temp_dir()
        
        # Read from temporary files
        current_path = os.path.join(temp_dir, 'current_weather.csv')
        forecast_path = os.path.join(temp_dir, 'forecast_weather.csv')
        
        current_df = pd.read_csv(current_path)
        forecast_df = pd.read_csv(forecast_path)
        
        # Create visualization directory
        viz_dir = os.path.join(AIRFLOW_HOME, 'visualizations')
        os.makedirs(viz_dir, exist_ok=True)
        
        # Create visualizations
        _visualize(current_df, forecast_df, output_dir=viz_dir)
        
        print("Visualizations created successfully")
        
    except Exception as e:
        logger.error(f"Error in visualize task: {str(e)}")
        raise

def run_load(**context):
    try:
        logger.info("Starting load process")
        # Get temp directory
        temp_dir = ensure_temp_dir()
        
        # Read from temporary files
        current_path = os.path.join(temp_dir, 'current_weather.csv')
        forecast_path = os.path.join(temp_dir, 'forecast_weather.csv')
        
        current_df = pd.read_csv(current_path)
        forecast_df = pd.read_csv(forecast_path)
        
        # Load to database
        _load(current_df, forecast_df)
        logger.info("Data loaded to database successfully")
        
    except Exception as e:
        logger.error(f"Error in load task: {str(e)}")
        raise

# Create tasks
extract_transform_task = PythonOperator(
    task_id='extract_transform',
    python_callable=run_extract_transform,
    dag=dag,
    provide_context=True
)

visualize_task = PythonOperator(
    task_id='visualize',
    python_callable=run_visualize,
    dag=dag,
    provide_context=True
)

load_task = PythonOperator(
    task_id='load',
    python_callable=run_load,
    dag=dag,
    provide_context=True
)

# Set dependencies
extract_transform_task >> [visualize_task, load_task]