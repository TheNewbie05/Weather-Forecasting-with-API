import logging
from src.api_client import fetch_weather_data
from src.validators import validate_weather_data
from database.database import get_connection
from config.config import CITIES

# Setup logging
logger = logging.getLogger(__name__)

def get_or_create_city(cursor, city_name):
    """Checks if city exists in MySQL 'cities' table, else creates it."""
    try:
        cursor.execute("SELECT city_id FROM cities WHERE city_name = %s", (city_name,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        
        cursor.execute("INSERT INTO cities (city_name) VALUES (%s)", (city_name,))
        return cursor.lastrowid
    except Exception as e:
        logger.error(f"Error in get_or_create_city for {city_name}: {e}")
        return None

def save_to_mysql(cursor, city_id, data):
    """Inserts validated weather data into MySQL 'weather_data' table."""
    try:
        query = """
            INSERT INTO weather_data 
            (city_id, timestamp, temperature_c, humidity, pressure_hpa, wind_speed_mps, weather_condition)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            city_id,
            data['timestamp'],
            data['temp'],
            data['humidity'],
            data['pressure'],
            data['wind_speed'],
            data['condition']
        )
        cursor.execute(query, values)
    except Exception as e:
        logger.error(f"Error inserting data for city_id {city_id}: {e}")
        raise e

def run_pipeline():
    """Main ETL Function: Extract -> Transform -> Load"""
    logger.info("--- ETL Pipeline Started ---")
    conn = get_connection()
    
    if not conn:
        logger.error("Pipeline aborted: Could not connect to MySQL.")
        return

    try:
        cursor = conn.cursor()
        for city in CITIES:
            # 1. EXTRACT
            raw_data = fetch_weather_data(city)
            
            if raw_data:
                # 2. TRANSFORM & VALIDATE
                validated_data = validate_weather_data(raw_data)
                
                if validated_data:
                    # 3. LOAD
                    city_id = get_or_create_city(cursor, city)
                    if city_id:
                        save_to_mysql(cursor, city_id, validated_data) # <--- YEH SIRF 1 BAAR HOGA
                        logger.info(f"✅ Data saved for {city}")
                        print(f"✅ Data saved for {city}")
        
        # Commit all changes at once
        conn.commit()
        logger.info("--- ETL Pipeline Completed Successfully ---")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Pipeline failed: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_pipeline()