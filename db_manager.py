import os
import sqlite3
import subprocess
import json
import time
import warnings
import africastalking
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()

# Secure credential extraction
USERNAME = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
API_KEY = os.getenv("AFRICASTALKING_API_KEY")

if not API_KEY:
    print("[SECURITY ALERT] Missing API key! Ensure .env file contains AFRICASTALKING_API_KEY")

africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

DB_NAME = "tracker.db"

def get_latest_meter_data(meter_number="37192840192"):
    """Fetches the latest meter units and consumption rate from SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meter_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meter_number TEXT NOT NULL,
            current_units REAL NOT NULL,
            daily_consumption REAL NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        SELECT current_units, daily_consumption 
        FROM meter_readings 
        WHERE meter_number = ? 
        ORDER BY updated_at DESC LIMIT 1
    ''', (meter_number,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"current_units": row[0], "daily_consumption": row[1]}
    else:
        # Default fallback values if no row exists yet
        return {"current_units": 2.2, "daily_consumption": 3.5}