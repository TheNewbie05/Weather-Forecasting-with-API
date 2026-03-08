import requests
import logging
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import API_KEY, BASE_URL  
from datetime import datetime, timezone, timedelta

# Set up logging for the API client
logger = logging.getLogger(__name__)

def fetch_weather_data(city):
    """
    Fetches real-time weather data for a specific city from OpenWeatherMap.
    Returns a dictionary of parsed data, or None if the request fails.
    """
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        # Request data from the API
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Raise an exception if the HTTP request returned an error status code
        response.raise_for_status()
        data = response.json()
        
        # Set Indian Standard Time (GMT+5:30)
        IST = timezone(timedelta(hours=5, minutes=30))
        
        # Format and return the extracted data
        return {
            'city': city,
            'timestamp': datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'condition': data['weather'][0]['description'],
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon']
        }
        
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred for {city}: {http_err}")
        print(f"❌ HTTP error for {city}. Check API Key or city name.")
        return None
        
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error occurred for {city}: {req_err}")
        print(f"❌ Network error for {city}. Check internet connection.")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error for {city}: {e}")
        return None

# Simple test block to check if the file works independently
if __name__ == "__main__":
    test_city = "New Delhi"
    print(f"⏳ Testing API connection for {test_city}...")
    result = fetch_weather_data(test_city)
    
    if result:
        print(f"✅ API Success! Temp in {test_city}: {result['temperature']}°C")
    else:
        print("❌ API Test Failed.")