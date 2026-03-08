import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.validators import validate_weather_data

def test_valid_weather_data():
    """Test with perfect data - should return True"""
    sample_data = {
        'city': 'Mumbai',
        'timestamp': '2026-03-08 10:00:00',
        'temperature': 30.5,
        'humidity': 65,
        'pressure': 1012,
        'wind_speed': 4.5,
        'condition': 'Haze',
        'latitude': 19.0760,   
        'longitude': 72.8777   
    }
    assert validate_weather_data(sample_data) is True

def test_extreme_temperature_c():
    """Test with impossible temperature_c - should return False"""
    bad_data = {
        'city': 'Mumbai',
        'temperature_c': 150,  
        'humidity': 50
    }
    assert validate_weather_data(bad_data) is False

def test_invalid_humidity():
    """Test with impossible humidity - should return False"""
    bad_data = {
        'city': 'Mumbai',
        'temperature_c': 25,
        'humidity': -10  # Impossible humidity
    }
    assert validate_weather_data(bad_data) is False

def test_missing_keys():
    """Test with missing data fields - should return False"""
    incomplete_data = {
        'city': 'Mumbai',
        'temperature_c': 25
        # missing humidity, condition, etc.
    }
    assert validate_weather_data(incomplete_data) is False