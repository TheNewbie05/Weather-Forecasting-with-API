import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.validators import validate_weather_data
from database.database import get_connection, setup_database
from config.config import DB_PATH

def test_database_connection():
    """Check if the database connection is successful"""
    conn = get_connection()
    assert conn is not None
    conn.close()

def test_table_structure():
    """Verify if the required tables exist in the database"""
    setup_database() # Ensure DB is created
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check for cities table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cities'")
    assert cursor.fetchone() is not None
    
    # Check for weather_data table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather_data'")
    assert cursor.fetchone() is not None
    
    conn.close()