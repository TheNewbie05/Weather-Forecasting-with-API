import requests
import time
from datetime import datetime, timedelta, timezone
from config.config import API_KEY

# Use the History API endpoint (One Call 3.0 or History API)
# Note: Ensure your API key supports historical data
HISTORY_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

def get_daily_historical_data(lat, lon, start_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    current_date = start_date
    
    # Stop at 'yesterday' because 2026 hasn't fully happened yet or to avoid future errors
    end_limit = datetime.now(timezone.utc)

    while current_date < end_limit:
        print(f"--- Fetching data for {current_date.date()} ---")
        
        # Calculate 10 timestamps for the day (one every 144 minutes)
        for i in range(10):
            timestamp = int(current_date.timestamp() + (i * 144 * 60))
            
            params = {
                'lat': lat,
                'lon': lon,
                'dt': timestamp,
                'appid': API_KEY,
                'units': 'metric'
            }

            try:
                response = requests.get(HISTORY_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Extracting specific data point
                weather = data['data'][0]
                print(f"[{i+1}] Time: {datetime.fromtimestamp(timestamp)} | Temp: {weather['temp']}°C")
                
                # Small sleep to respect API rate limits
                time.sleep(0.1) 
                
            except Exception as e:
                print(f"❌ Error at {timestamp}: {e}")
                break
        
        # Move to the next day
        current_date += timedelta(days=1)

if __name__ == "__main__":
    # Example: New Delhi Coordinates
    LAT, LON = 28.6139, 77.2090 
    get_daily_historical_data(LAT, LON, "2025-04-01")