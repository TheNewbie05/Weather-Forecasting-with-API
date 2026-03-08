"""
Configuration settings for the Weather Data Pipeline
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 📂 DIRECTORY & PATHS CONFIGURATION
# ==========================================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DB_PATH = os.path.join(ROOT_DIR, 'database', 'weather_data.db')
REPORT_DIR = os.path.join(ROOT_DIR, 'reports')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'pipeline.log')

# Auto-create necessary folders so we never get "Folder Not Found" error
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, 'database'), exist_ok=True)

# ==========================================
# 🛰️ API CONFIGURATION
# ==========================================
API_KEY = os.getenv("API_KEY", "c90e8628330ee3aedd8cde23f8cfd65f")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# ==========================================
# 🌍 TARGET CITIES
# ==========================================
CITIES = [
    'New Delhi', 'Kolkata', 'Mumbai', 'Bengaluru', 'Chennai',
    'Hyderabad', 'Ahmedabad', 'Surat', 'Pune', 'Jaipur', 'Lucknow',
    'Kanpur', 'Nagpur', 'Indore', 'Thane'
]
# Scheduling Configuration
SCHEDULE_INTERVAL = timedelta(hours=1)  # Run every hour
SCHEDULE_TIME = '00:00'  # Time to run daily scheduled tasks

# Data Quality Thresholds
TEMPERATURE_MIN = -50.0
TEMPERATURE_MAX = 60.0
HUMIDITY_MIN = 0
HUMIDITY_MAX = 100
PRESSURE_MIN = 900.0
PRESSURE_MAX = 1100.0
WIND_SPEED_MAX = 150.0

# Alert Thresholds
TEMP_HIGH_THRESHOLD = 30.0  # Celsius
HUMIDITY_HIGH_THRESHOLD = 75  # Percentage
PRESSURE_LOW_THRESHOLD = 1000.0  # hPa

# Logging Configuration
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'pipeline.log')
LOG_LEVEL = 'INFO'

# Report Configuration
REPORT_DIR = os.path.join(os.path.dirname(__file__), 'reports')
REPORT_FORMAT = 'csv'  # csv, json, html

# Retention Policy
DATA_RETENTION_DAYS = 90  # Keep 90 days of data