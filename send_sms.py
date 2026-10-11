import os
import africastalking
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

USERNAME = os.getenv("AFRICASTALKING_USERNAME")
API_KEY = os.getenv("AFRICASTALKING_API_KEY")

# Initialize Africa's Talking
africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

def send_alert_sms(phone_number, message):
    """Sends an SMS alert via Africa's Talking API without console fallbacks."""
    try:
        response = sms.send(message, [phone_number])
        print(f"SUCCESS: SMS sent to {phone_number} -> {response}")
        return True
    except Exception as error:
        print(f"ERROR: Could not send SMS to {phone_number}. Details: {error}")
        return False