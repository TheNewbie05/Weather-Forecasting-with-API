import pandas as pd
import sqlite3
import os
import csv
import logging
from datetime import datetime
from database.database import get_connection    # <-- Updated
from config.config import REPORT_DIR            # <-- Updated

logger = logging.getLogger(__name__)
def generate_report():
    print("⏳ Generating report...")
    
    # 1. Connect to the SQLite database
    try:
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return

    # 2. Extract data by joining the cities and weather_data tables
    query = """
        SELECT 
            cities.city_name,
            weather_data.timestamp,
            weather_data.temperature_c,
            weather_data.humidity,
            weather_data.pressure_hpa,
            weather_data.wind_speed_mps,
            weather_data.weather_condition
        FROM weather_data
        JOIN cities ON weather_data.city_id = cities.city_id
        ORDER BY weather_data.timestamp DESC
    """
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        
        # Stop if the database is empty
        if not records:
            print("⚠️ No data found in the database. Please run call_api.py first!")
            return

        # 3. Set up the CSV filename and path
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"weather_report_{current_date}.csv"
        filepath = os.path.join(REPORT_DIR, filename)

        # 4. Save the data into a CSV file
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the column headers first
            writer.writerow(['City Name', 'Timestamp', 'Temperature (C)', 'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (m/s)', 'Condition'])
            
            # Write the actual data rows
            writer.writerows(records)

        print(f"✅ CSV Report generated successfully!\n📁 File saved at: {filepath}")

    except Exception as e:
        print(f"❌ Error occurred while generating report: {e}")
        
    finally:
        # Always close the database connection
        conn.close()

if __name__ == "__main__":
    generate_report()