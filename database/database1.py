import mysql.connector # SQLite ki jagah MySQL connector
import logging
import os 
import sys
from mysql.connector import Error

# Path setup for config imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import API_KEY, BASE_URL 

# Setup basic logging
logger = logging.getLogger(__name__)

# --- MySQL Configuration ---
# Aap in details ko config.py mein bhi daal sakte hain
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',         # Apna MySQL username check karein
    'password': 'root', # Apna password yahan likhein
    'database': 'weather_db'     # Pehle MySQL Workbench mein ye DB bana lijiye
}

def get_connection():
    """ Creates and returns a connection to the MySQL database. """
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        logger.error(f"MySQL Connection failed: {e}")
        print(f"❌ Connection error: {e}")
        return None

def setup_database():
    """ Creates the required tables in MySQL if they do not exist. """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    try:
        # 1. Create cities table
        cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                            city_id INT AUTO_INCREMENT PRIMARY KEY,
                            city_name VARCHAR(100) NOT NULL UNIQUE,
                            country VARCHAR(50),
                            latitude DECIMAL(10, 8),
                            longitude DECIMAL(11, 8),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        
        # 2. Create weather_data table
        cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                            record_id INT AUTO_INCREMENT PRIMARY KEY,
                            city_id INT,
                            timestamp DATETIME,
                            temperature_c DECIMAL(5, 2),
                            humidity INT,
                            pressure_hpa DECIMAL(6, 2),
                            wind_speed_mps DECIMAL(5, 2),
                            weather_condition VARCHAR(100),
                            FOREIGN KEY (city_id) REFERENCES cities(city_id)
                        )''')
        
        conn.commit()
        print("✅ MySQL tables verified/created successfully.")
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        logger.error(f"Error creating tables: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()