import sqlite3
import random
from datetime import datetime, timedelta

# Apne database ka path check kar lein
db_path = r'database\weather_data.db'

def generate_yearly_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT city_id, city_name FROM cities")
    cities = cursor.fetchall()

    if not cities:
        print("❌ 'cities' table khali hai! Pehle API se cities aane dein.")
        return

    print("⏳ Generating 1 YEAR of realistic seasonal weather data...")
    print("Isme 10-15 seconds lag sakte hain, kripya wait karein...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # Pure 1 saal peeche
    
    insert_query = """
        INSERT INTO weather_data 
        (city_id, timestamp, temperature_c, humidity, pressure_hpa, wind_speed_mps, weather_condition)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    total_records = 0
    current_date = start_date

    while current_date <= end_date:
        month = current_date.month # Konsa mahina chal raha hai
        
        # Din mein 4 baar ka data (Subah, Dopehar, Shaam, Raat)
        for hour in [6, 14, 18, 22]:
            record_time = current_date.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))
            timestamp_str = record_time.strftime('%Y-%m-%d %H:%M:%S')

            for city_id, city_name in cities:
                # 1. Base Annual Average (Normal din kaisa hota hai)
                if city_name in ['Mumbai', 'Chennai', 'Kolkata', 'Surat', 'Thane']: 
                    base_temp, base_hum = 30, 75
                elif city_name in ['New Delhi', 'Jaipur', 'Lucknow', 'Kanpur']: 
                    base_temp, base_hum = 28, 45
                elif city_name == 'Bengaluru': 
                    base_temp, base_hum = 24, 60
                else: 
                    base_temp, base_hum = 27, 55
                
                # 2. Season ke hisaab se logic (Asli Jadoo Yahan Hai 🪄)
                condition = "Clear"
                if month in [3, 4, 5, 6]: # Summer (Garmi)
                    base_temp += random.uniform(5, 10)
                    base_hum -= random.uniform(5, 15)
                    condition = random.choice(["Clear", "Haze", "Sunny"])
                    if city_name in ['New Delhi', 'Jaipur']: base_temp += 5 # North mein extreme garmi
                        
                elif month in [7, 8, 9]: # Monsoon (Baarish)
                    base_temp -= random.uniform(0, 4)
                    base_hum += random.uniform(15, 25)
                    condition = random.choice(["Rain", "Thunderstorm", "Clouds", "Overcast"])
                    
                else: # Winter (Sardi - Oct to Feb)
                    base_temp -= random.uniform(8, 15)
                    if city_name in ['New Delhi', 'Jaipur', 'Lucknow']: base_temp -= 5 # North mein extreme sardi
                    condition = random.choice(["Mist", "Fog", "Clear", "Smoke"])
                    
                # 3. Time ke hisaab se (Dopehar mein peak garmi, subah thand)
                if hour == 14: base_temp += random.uniform(3, 6) 
                elif hour == 6: base_temp -= random.uniform(2, 5) 
                
                # Limit check taaki percentages over 100 na jayein
                base_hum = min(100, max(10, base_hum)) 
                
                # Randomize pressure and wind
                pressure = random.randint(1000, 1020)
                wind = round(random.uniform(1.0, 8.0), 2)
                
                cursor.execute(insert_query, (
                    city_id, timestamp_str, round(base_temp, 2), round(base_hum), pressure, wind, condition
                ))
                total_records += 1
                
        current_date += timedelta(days=1)

    conn.commit()
    conn.close()
    print(f"✅ BINGO! {total_records} records inserted successfully for the LAST 1 YEAR.")

if __name__ == "__main__":
    generate_yearly_data()