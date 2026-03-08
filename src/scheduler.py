import schedule
import time
import logging
from src.etl_pipeline import run_pipeline
from src.reporter import generate_report

logger = logging.getLogger(__name__)

def start_automation():
    print("🚀 Initializing Automation...")
    
    # 1. Pipeline ko sirf EK BAAR schedule karein
    schedule.every(1).hours.do(run_pipeline)
    
    # 2. Report ko bhi sirf EK BAAR schedule karein
    schedule.every().day.at("15:13").do(generate_report)
    
    print("==================================================")
    print("🚀 Automation Engine is now RUNNING!")
    print("📍 ETL: Every 1 Hour")
    print("⚠️ Keep this terminal open to stay on Autopilot.")
    print("==================================================")
    
    # First run manual (Taaki turant data aa jaye, uske baad scheduler sambhalega)
    run_pipeline()
    
    # Loop jo scheduler ko chalata rahega
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_automation()