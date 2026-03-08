import sqlite3
import logging
import requests
import logging
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import API_KEY, BASE_URL ,DB_PATH  
from datetime import datetime, timezone, timedelta
# Setup basic logging for the database module
logger = logging.getLogger(__name__)

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def setup_database():
    """
    Creates the required tables (cities and weather_data) if they do not exist.
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    try:
        # Create cities table with a UNIQUE constraint to prevent duplicates
        cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                            city_id INTEGER PRIMARY KEY,
                            city_name TEXT NOT NULL UNIQUE,
                            country TEXT,
                            latitude REAL,
                            longitude REAL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        
        # Create weather_data table with a Foreign Key linked to cities
        cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                            record_id INTEGER PRIMARY KEY,
                            city_id INTEGER,
                            timestamp TIMESTAMP,
                            temperature_c REAL,
                            humidity INTEGER,
                            pressure_hpa REAL,
                            wind_speed_mps REAL,
                            weather_condition TEXT,
                            FOREIGN KEY (city_id) REFERENCES cities (city_id)
                        )''')
        
        conn.commit()
        print("✅ Database tables verified/created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        logger.error(f"Error creating tables: {e}")
    finally:
        # Always close the connection
        conn.close()

# If you run this file directly, it will verify/create the tables
if __name__ == "__main__":
    setup_database()