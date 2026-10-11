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
    raise ValueError("[SECURITY ALERT] Missing API key! Ensure .env file contains AFRICASTALKING_API_KEY.")

africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

CPP_EXECUTABLE = "./tracker.exe" if os.name == 'nt' else "./tracker_engine"


def mask_phone(phone: str) -> str:
    """Masks phone numbers for logging privacy (e.g., +2547****5206)."""
    if len(phone) >= 10:
        return phone[:5] + "****" + phone[-4:]
    return phone


def send_alert_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print(f"[SMS SENT] To Buyer: {mask_phone(phone_number)}")
        return response
    except Exception as e:
        print(f"[SMS FAILED] To: {mask_phone(phone_number)} | Error: {e}")
        return None


def run_tracker_checks():
    print("\n--- [SECURE GATEWAY] Running encrypted checks... ---")
    
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Parameterized query to prevent SQL Injection
    cursor.execute("SELECT meter_number, buyer_phone, balance, daily_usage FROM token_transactions")
    records = cursor.fetchall()

    for record in records:
        meter_number, buyer_phone, balance, daily_usage = record

        # Input sanitization before passing to C++ subprocess
        clean_meter = str(meter_number).strip()
        clean_phone = str(buyer_phone).strip()
        clean_balance = str(float(balance))
        clean_usage = str(float(daily_usage))

        try:
            # Secure subprocess execution (avoids shell=True to prevent command injection)
            result = subprocess.run(
                [CPP_EXECUTABLE, clean_meter, clean_phone, clean_balance, clean_usage],
                capture_output=True,
                text=True,
                check=True
            )
            
            output = json.loads(result.stdout.strip())
            
            new_balance = float(output["new_balance"])
            time_left = str(output["time_left"])
            needs_alert = bool(output["needs_alert"])

            # Parameterized update statement
            cursor.execute("""
                UPDATE token_transactions 
                SET balance = ?, last_updated = CURRENT_TIMESTAMP 
                WHERE meter_number = ?
            """, (new_balance, clean_meter))

            print(f"Meter: {clean_meter} | Buyer: {mask_phone(clean_phone)} | Bal: {new_balance}u | Time Left: {time_left}")

            if needs_alert:
                print(f"--> [ALERT TRIGGERED] Sending SMS to buyer {mask_phone(clean_phone)}...")
                msg = f"KPLC Alert: Meter {clean_meter} token balance is low ({new_balance} units remaining). Est time left: {time_left}. Top up to avoid blackout."
                send_alert_sms(clean_phone, msg)

                # Parameterized insertion for audit logs
                cursor.execute("""
                    INSERT INTO alert_logs (meter_number, buyer_phone, balance_at_alert)
                    VALUES (?, ?, ?)
                """, (clean_meter, clean_phone, new_balance))

        except Exception as err:
            print(f"[ENGINE ERROR] Failed processing meter {clean_meter}: {err}")

    conn.commit()
    conn.close()
    print("--- [CHECK COMPLETE] Enterprise Database & C++ Engine Synced. ---\n")


if __name__ == "__main__":
    print("Starting Commercial Multi-User Tracker Gateway...")
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_tracker_checks, 'interval', seconds=60)
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Stopping gateway safely...")
        scheduler.shutdown()
if __name__ == "__main__":
    print("=====================================")
    print(" Starting KPLC Enterprise Token Monitoring Service")
    print(" Architecture: Python Gateway -> C++ Math Core")
    print("=====================================")
    
    scheduler = BackgroundScheduler()
    # Runs automated checks every 60 seconds
    scheduler.add_job(run_tracker_checks, 'interval', seconds=60)
    scheduler.start()
    
    try:
        # Keep the service running continuously
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\n[SHUTDOWN] Gracefully stopping scheduler and closing gateway...")
        scheduler.shutdown()
        print("[SHUTDOWN] Service stopped successfully.")