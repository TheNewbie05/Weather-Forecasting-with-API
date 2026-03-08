import os
import sqlite3
import logging
from datetime import datetime
from config.config import DB_PATH, LOG_FILE     # <-- Updated

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
# Setup logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_system_health():
    """Checks the database status and logs the system health."""
    print("\n🔍 Checking System Health...")
    
    if not os.path.exists(DB_PATH):
        print("❌ Error: Database file missing!")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Count total records
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        total_records = cursor.fetchone()[0]
        
        # 2. Get last update time
        cursor.execute("SELECT MAX(timestamp) FROM weather_data")
        last_update = cursor.fetchone()[0]
        
        # 3. Count unique cities
        cursor.execute("SELECT COUNT(*) FROM cities")
        total_cities = cursor.fetchone()[0]
        
        conn.close()

        status_msg = (
            f"✅ System Healthy | "
            f"Cities: {total_cities} | "
            f"Total Records: {total_records} | "
            f"Last Update: {last_update if last_update else 'No Data'}"
        )
        print(status_msg)
        logger.info(status_msg)
        return True

    except Exception as e:
        print(f"❌ System Health Check Failed: {e}")
        logger.error(f"Health check error: {e}")
        return False

if __name__ == "__main__":
    check_system_health()