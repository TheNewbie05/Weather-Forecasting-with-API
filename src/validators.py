import logging
from src.api_client import fetch_weather_data
from database.database import get_connection
from config.config import CITIES
from src.api_client import fetch_weather_data

# Setup logging
logger = logging.getLogger(__name__)

def validate_weather_data(data):
    """
    Loads the transformed weather data into the SQLite database.
    """
    if not data:
        return False
        
    conn = get_connection()
    if not conn:
        logger.error("Could not connect to database for loading.")
        return False
        
    cursor = conn.cursor()
    
    try:
        # 1. Insert City (Ignore if it already exists)
        cursor.execute("""
            INSERT OR IGNORE INTO cities (city_name, country, latitude, longitude)
            VALUES (?, 'India', ?, ?)
        """, (data['city'], data['latitude'], data['longitude']))
        
        conn.commit()

        # 2. Get the city_id for the foreign key
        cursor.execute("SELECT city_id FROM cities WHERE city_name = ?", (data['city'],))
        city_id_result = cursor.fetchone()
        
        if not city_id_result:
            logger.error(f"Could not find city_id for {data['city']}")
            return False
            
        city_id = city_id_result[0]
        
        # 3. Insert the Weather Data safely
        cursor.execute("""
            INSERT INTO weather_data(city_id, timestamp, temperature_c, humidity, pressure_hpa, wind_speed_mps, weather_condition)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (city_id, data['timestamp'], data['temperature'], data['humidity'], 
              data['pressure'], data['wind_speed'], data['condition']))
        
        conn.commit()
        logger.info(f"Successfully loaded data for {data['city']}")
        print(f"✅ Data saved for {data['city']} at {data['timestamp']} IST")
        return True
        
    except Exception as e:
        logger.error(f"Error loading data for {data['city']}: {e}")
        print(f"❌ Failed to save data for {data['city']}: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def run_pipeline():
    """
    The main ETL (Extract, Transform, Load) workflow.
    Iterates through all configured cities.
    """
    print("\n🚀 Starting ETL Pipeline...")
    success_count = 0
    
    for city in CITIES:
        # EXTRACT: Get data from API
        weather_data = fetch_weather_data(city)
        
        # TRANSFORM & LOAD: Save to Database
        if weather_data:
            if validate_weather_data(weather_data):
                success_count += 1
                
    print(f"\n🎉 Pipeline Finished! Successfully updated {success_count}/{len(CITIES)} cities.")

# Test the pipeline
if __name__ == "__main__":
    run_pipeline()