## Overview
This project implements an ETL (Extract, Transform, Load) pipeline for weather data using OpenWeather API. It collects current weather data and 5-day forecasts for specified cities, processes the data, and stores it in a PostgreSQL database. The pipeline is orchestrated using Apache Airflow.

## System Setup

### 1. WSL Installation (Windows)
```powershell
# Open PowerShell as Administrator and run:
wsl --install

# After installation, restart your computer and open Ubuntu
```

### 2. Basic Ubuntu Setup
```bash
# Update package list and upgrade existing packages
sudo apt update
sudo apt upgrade -y

# Install Python and related tools
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-venv -y
```

### 3. Python Virtual Environment Setup
```bash
# Create virtual environment
python3 -m venv airflow_env

# Activate virtual environment
source airflow_env/bin/activate

# Install required Python packages
pip install apache-airflow
pip install python-dotenv pandas requests psycopg2-binary matplotlib seaborn
```

### 4. PostgreSQL Installation and Setup
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql -c "CREATE USER airflow WITH PASSWORD 'airflow' SUPERUSER;"
sudo -u postgres psql -c "CREATE DATABASE weather_db OWNER airflow;"

# Verify connection
PGPASSWORD=airflow psql -U airflow -h localhost -d weather_db
```

### 5. Database Schema Setup
Connect to the database and create the required tables:

```sql
-- Connect to database
PGPASSWORD=airflow psql -U airflow -h localhost -d weather_db

-- Create tables
CREATE TABLE current_weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50) UNIQUE NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure FLOAT,
    humidity INTEGER,
    weather_desc VARCHAR(100),
    wind_speed FLOAT,
    wind_deg INTEGER,
    clouds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE forecast_weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    forecast_timestamp TIMESTAMP NOT NULL,
    temperature FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure FLOAT,
    humidity INTEGER,
    weather_desc VARCHAR(100),
    wind_speed FLOAT,
    wind_deg INTEGER,
    clouds INTEGER,
    pop FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city, forecast_timestamp)
);
```

## Project Setup

### 1. Clone Repository (On Windows)
```powershell
# Open PowerShell and navigate to desired location
cd C:\Users\YourUsername\Documents  # or any preferred location
# Clone the repository
git clone https://github.com/Shanmukhi1920/ETL-MiniProject.git
```
### 2. Directory Setup in WSL
```bash
# Create necessary directories in WSL
mkdir -p ~/airflow/dags ~/airflow/src ~/airflow/temp ~/airflow/visualizations
```

### 3. Copy Files from Windows to WSL
```bash
# Navigate to your Windows directory in WSL where you cloned the repo
cd /mnt/c/Users/YourUsername/Documents/weather-etl

# Copy files to respective directories in Airflow
cp weather_dag.py ~/airflow/dags/
cp src/extract.py src/transform.py src/load.py src/validate.py src/visualize.py ~/src
``` 
### 4. Environment Setup
Open .bashrc file
```bash
nano ~/.bashrc
```

Add the following content:
```
weather_api_key='your_api_key_here'
```
Save and exit (Ctrl + X, then Y, then Enter)

Apply the changes:
```bash
source ~/.bashrc
```

### 5. Airflow Configuration
```bash
# Set Airflow home
export AIRFLOW_HOME=~/airflow

# Initialize the database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname YourName \
    --lastname YourLastName \
    --role Admin \
    --email your@email.com \
    --password admin
```

## Running the Pipeline

### 1. Start Airflow Services
Open two separate terminals and run:

Terminal 1:
```bash
# Activate virtual environment
source airflow_env/bin/activate

# Start webserver
airflow webserver
```

Terminal 2:
```bash
# Activate virtual environment
source airflow_env/bin/activate

# Start scheduler
airflow scheduler
```

### 2. Access Airflow UI
- Open a web browser and go to: `http://localhost:8080`
- Login with the admin credentials you created

### 3. Running the DAG
1. In the Airflow UI, find the 'weather_etl' DAG
2. Toggle the DAG switch to "On"
3. Click on the "Trigger DAG" button to run manually
4. Monitor the task execution in the "Grid" view

## Monitoring and Maintenance

### Check Database Data
```bash
# Connect to database
PGPASSWORD=airflow psql -U airflow -h localhost -d weather_db

# View current weather data
SELECT * FROM current_weather ORDER BY timestamp DESC LIMIT 5;

# View forecast data
SELECT * FROM forecast_weather ORDER BY forecast_timestamp DESC LIMIT 5;
```

### View Visualizations
Check the generated visualizations in:
```bash
ls -l ~/airflow/visualizations/
```

### Check Logs
```bash
# View Airflow task logs
cd ~/airflow/logs/weather_etl/
```
