import logging
import os
import sys

# Path setup (agar root folder se direct run na ho toh backup ke liye)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import LOG_FILE
from database.database import setup_database
from src.monitor import check_system_health
from src.scheduler import start_automation

# --- Setup Logging ---
# (Yahan main terminal output aur file output ko alag kar raha hu taaki console par double print na ho)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8') # Logs sirf pipeline.log file mein jayenge
    ]
)

logger = logging.getLogger(__name__)

def main():
    print("==================================================")
    print("        🌤️  WEATHER ETL PIPELINE v1.0  🌤️        ")
    print("==================================================")
    
    # 1. Database Setup (MySQL tables verify/create karega)
    setup_database()
    
    # 2. Health Check (Check karega connection aur records)
    is_healthy = check_system_health()
    
    if not is_healthy:
        print("❌ System health check failed. Please check MySQL connection. Exiting...")
        return

    # 3. Start Automation (Control scheduler ko dega)
    print("\n🚀 Starting automation schedule (Press Ctrl+C to stop)...")
    try:
        # start_automation() ke andar hi pehli baar pipeline run hogi aur phir schedule hogi
        start_automation() 
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user. Goodbye!")
        logger.info("System manually stopped by user.")

if __name__ == "__main__":
    main()